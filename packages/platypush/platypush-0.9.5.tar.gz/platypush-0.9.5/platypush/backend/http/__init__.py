import asyncio
import datetime
import dateutil.parser
import inspect
import json
import os
import re
import time

from threading import Thread, get_ident
from multiprocessing import Process
from flask import Flask, Response, abort, jsonify, request as http_request, \
    render_template, send_from_directory

from redis import Redis

from platypush.config import Config
from platypush.context import get_backend, get_or_create_event_loop
from platypush.message import Message
from platypush.message.event import Event, StopEvent
from platypush.message.event.web.widget import WidgetUpdateEvent
from platypush.message.request import Request
from platypush.utils import get_ssl_server_context, set_thread_name

from .. import Backend


class HttpBackend(Backend):
    """
    The HTTP backend is a general-purpose web server that you can leverage:

        * To execute Platypush commands via HTTP calls. Example::

            curl -XPOST -H 'Content-Type: application/json' -H "X-Token: your_token" \\
                -d '{
                    "type":"request",
                    "target":"nodename",
                    "action":"tts.say",
                    "args": {"phrase":"This is a test"}
                }' \\
                http://localhost:8008/execute

        * To interact with your system (and control plugins and backends) through the Platypush web panel, by default available on your web root document. Any plugin that you have configured and available as a panel plugin will appear on the web panel as well as a tab.

        * To display a fullscreen dashboard with your configured widgets, by default available under ``/dashboard``

    Note that if you set up a main token, it will be required for any HTTP
    interaction - either as ``X-Token`` HTTP header, on the query string
    (attribute name: ``token``), as part of the JSON payload root (attribute
    name: ``token``), or via HTTP basic auth (any username works).

    Requires:

        * **flask** (``pip install flask``)
        * **redis** (``pip install redis``)
        * **websockets** (``pip install websockets``)
        * **python-dateutil** (``pip install python-dateutil``)
    """

    hidden_plugins = {
        'assistant.google'
    }

    def __init__(self, port=8008, websocket_port=8009, disable_websocket=False,
                 redis_queue='platypush/http', dashboard={}, resource_dirs={},
                 ssl_cert=None, ssl_key=None, ssl_cafile=None, ssl_capath=None,
                 maps={}, **kwargs):
        """
        :param port: Listen port for the web server (default: 8008)
        :type port: int

        :param websocket_port: Listen port for the websocket server (default: 8009)
        :type websocket_port: int

        :param disable_websocket: Disable the websocket interface (default: False)
        :type disable_websocket: bool

        :param redis_queue: Name of the Redis queue used to synchronize messages with the web server process (default: ``platypush/http``)
        :type redis_queue: str

        :param ssl_cert: Set it to the path of your certificate file if you want to enable HTTPS (default: None)
        :type ssl_cert: str

        :param ssl_key: Set it to the path of your key file if you want to enable HTTPS (default: None)
        :type ssl_key: str

        :param ssl_cafile: Set it to the path of your certificate authority file if you want to enable HTTPS (default: None)
        :type ssl_cafile: str

        :param ssl_capath: Set it to the path of your certificate authority directory if you want to enable HTTPS (default: None)
        :type ssl_capath: str

        :param resource_dirs: Static resources directories that will be
            accessible through ``/resources/<path>``. It is expressed as a map
            where the key is the relative path under ``/resources`` to expose and
            the value is the absolute path to expose.
        :type resource_dirs: dict[str, str]

        :param dashboard: Set it if you want to use the dashboard service. It will contain the configuration for the widgets to be used (look under ``platypush/backend/http/templates/widgets/`` for the available widgets).

        Example configuration::

            dashboard:
                background_image: https://site/image.png
                widgets:                # Each row of the dashboard will have 6 columns
                    calendar:           # Calendar widget
                        columns: 6
                    music:              # Music widget
                        columns: 3
                    date-time-weather:  # Date, time and weather widget
                        columns: 3
                    image-carousel:     # Image carousel
                        columns: 6
                        images_path: ~/Dropbox/Photos/carousel  # Absolute path (valid as long as it's a subdirectory of one of the available `resource_dirs`)
                        refresh_seconds: 15
                    rss-news:           # RSS feeds widget
                        # Requires backend.http.poll to be enabled with some RSS sources and write them to sqlite db
                        columns: 6
                        limit: 25
                        db: "sqlite:////home/blacklight/.local/share/platypush/feeds/rss.db"

        :type dashboard: dict
        """

        super().__init__(**kwargs)

        self.port = port
        self.websocket_port = websocket_port
        self.redis_queue = redis_queue
        self.dashboard = dashboard
        self.maps = maps
        self.server_proc = None
        self.disable_websocket = disable_websocket
        self.websocket_thread = None
        self.redis_thread = None
        self.redis = None
        self.resource_dirs = { name: os.path.abspath(
            os.path.expanduser(d)) for name, d in resource_dirs.items() }
        self.active_websockets = set()
        self.ssl_context = get_ssl_server_context(ssl_cert=ssl_cert,
                                                  ssl_key=ssl_key,
                                                  ssl_cafile=ssl_cafile,
                                                  ssl_capath=ssl_capath) \
            if ssl_cert else None


    def send_message(self, msg):
        self.logger.warning('Use cURL or any HTTP client to query the HTTP backend')


    def stop(self):
        """ Stop the web server """
        self.logger.info('Received STOP event on HttpBackend')

        if self.redis_thread:
            stop_evt = StopEvent(target=self.device_id, origin=self.device_id,
                                 thread_id=self.redis_thread.ident)

            redis = self._get_redis()
            if redis:
                redis.rpush(self.redis_queue, str(stop_evt))

        if self.server_proc:
            self.server_proc.terminate()
            self.server_proc.join()

    def notify_web_clients(self, event):
        """ Notify all the connected web clients (over websocket) of a new event """
        import websockets

        async def send_event(websocket):
            try:
                await websocket.send(str(event))
            except Exception as e:
                self.logger.warning('Error on websocket send_event: {}'.format(e))

        loop = get_or_create_event_loop()

        for websocket in self.active_websockets:
            try:
                loop.run_until_complete(send_event(websocket))
            except websockets.exceptions.ConnectionClosed:
                self.logger.info('Client connection lost')
                self.active_websockets.remove(websocket)


    def redis_poll(self):
        """ Polls for new messages on the internal Redis queue """

        while not self.should_stop():
            redis = self._get_redis()
            if not redis:
                continue

            msg = redis.blpop(self.redis_queue)
            msg = Message.build(json.loads(msg[1].decode('utf-8')))
            self.on_message(msg)


    @classmethod
    def _authenticate(cls):
        return Response('Authentication required', 401,
                        {'WWW-Authenticate': 'Basic realm="Login required"'})

    @classmethod
    def _authentication_ok(cls):
        token = Config.get('token')
        if not token:
            return True

        user_token = None

        # Check if
        if 'X-Token' in http_request.headers:
            user_token = http_request.headers['X-Token']
        elif http_request.authorization:
            # TODO support for user check
            user_token = http_request.authorization.password
        elif 'token' in http_request.args:
            user_token = http_request.args.get('token')
        else:
            try:
                args = json.loads(http_request.data.decode('utf-8'))
                user_token = args.get('token')
            except:
                pass

        if user_token == token:
            return True

        return False

    def webserver(self):
        """ Web server main process """
        set_thread_name('WebServer')

        basedir = os.path.dirname(inspect.getfile(self.__class__))
        template_dir = os.path.join(basedir, 'templates')
        app = Flask(__name__, template_folder=template_dir)
        self.redis_thread = Thread(target=self.redis_poll)
        self.redis_thread.start()

        @app.route('/execute', methods=['POST'])
        def execute():
            """ Endpoint to execute commands """
            if not self._authentication_ok(): return self._authenticate()

            args = json.loads(http_request.data.decode('utf-8'))
            msg = Message.build(args)
            self.logger.info('Received message on the HTTP backend: {}'.format(msg))

            if Config.get('token'):
                msg.token = Config.get('token')

            if isinstance(msg, Request):
                msg.backend = self
                msg.origin = 'http'

            self.bus.post(msg)

            if isinstance(msg, Request):
                response = self.get_message_response(msg)
                self.logger.info('Processing response on the HTTP backend: {}'.format(response))
                if response:
                    return Response(str(response), mimetype='application/json')

        @app.route('/')
        def index():
            """ Route to the main web panel """
            if not self._authentication_ok(): return self._authenticate()

            configured_plugins = Config.get_plugins()
            enabled_plugins = {}
            hidden_plugins = {}

            for plugin, conf in configured_plugins.items():
                template_file = os.path.join('plugins', plugin + '.html')
                if os.path.isfile(os.path.join(template_dir, template_file)):
                    if plugin in self.hidden_plugins:
                        hidden_plugins[plugin] = conf
                    else:
                        enabled_plugins[plugin] = conf

            return render_template('index.html', plugins=enabled_plugins,
                                   hidden_plugins=hidden_plugins, utils=HttpUtils,
                                   token=Config.get('token'),
                                   websocket_port=self.websocket_port,
                                   has_ssl=self.ssl_context is not None)


        @app.route('/widget/<widget>', methods=['POST'])
        def widget_update(widget):
            """ ``POST /widget/<widget_id>`` will update the specified widget_id on the dashboard with the specified key-values """
            event = WidgetUpdateEvent(
                widget=widget, **(json.loads(http_request.data.decode('utf-8'))))

            redis = self._get_redis()
            if redis:
                redis.rpush(self.redis_queue, str(event))
            return jsonify({ 'status': 'ok' })

        @app.route('/resources/<path:path>', methods=['GET'])
        def static_path(path):
            """ Static resources """
            base_path = os.path.dirname(path).split('/')
            while base_path:
                if os.sep.join(base_path) in self.resource_dirs:
                    break
                base_path.pop()

            if not base_path:
                abort(404)

            base_path = os.sep.join(base_path)
            real_base_path = self.resource_dirs[base_path]
            real_path = real_base_path

            file_path = [s for s in
                         re.sub(r'^{}(.*)$'.format(base_path), '\\1', path) \
                         .split('/') if s]

            for p in file_path[:-1]:
                real_path += os.sep + p
                file_path.pop(0)

            file_path = file_path.pop(0)
            if not real_path.startswith(real_base_path):
                # Directory climbing attempt
                abort(404)

            return send_from_directory(real_path, file_path)

        @app.route('/dashboard', methods=['GET'])
        def dashboard():
            """ Route for the fullscreen dashboard """
            if not self._authentication_ok(): return self._authenticate()

            return render_template('dashboard.html', config=self.dashboard, utils=HttpUtils,
                                   token=Config.get('token'), websocket_port=self.websocket_port)

        @app.route('/map', methods=['GET'])
        def map():
            """
            Query parameters:
                start -- Map timeline start timestamp
                end   -- Map timeline end timestamp
                zoom  -- Between 1-20. Set it if you want to override the
                    Google's API auto-zoom. You may have to set it if you are
                    trying to embed the map into an iframe

            Supported values for `start` and `end`:
                - now
                - yesterday
                - -30s (it means '30 seconds ago')
                - -10m (it means '10 minutes ago')
                - -24h (it means '24 hours ago')
                - -7d  (it means '7 days ago')
                - 2018-06-04T17:39:22.742Z (ISO strings)

            Default: start=yesterday, end=now
            """

            def parse_time(time_string):
                if not time_string:
                    return None

                now = datetime.datetime.now()

                if time_string == 'now':
                    return now.isoformat()
                if time_string == 'yesterday':
                    return (now - datetime.timedelta(days=1)).isoformat()

                try:
                    return dateutil.parser.parse(time_string).isoformat()
                except ValueError:
                    pass

                m = re.match('([-+]?)([0-9]+)([dhms])', time_string)
                if not m:
                    raise RuntimeError('Invalid time interval string representation: "{}"'.
                                    format(time_string))

                time_delta = (-1 if m.group(1) == '-' else 1) * int(m.group(2))
                time_unit = m.group(3)

                if time_unit == 'd':
                    params = { 'days': time_delta }
                elif time_unit == 'h':
                    params = { 'hours': time_delta }
                elif time_unit == 'm':
                    params = { 'minutes': time_delta }
                elif time_unit == 's':
                    params = { 'seconds': time_delta }

                return (now + datetime.timedelta(**params)).isoformat()


            if not self._authentication_ok(): return self._authenticate()

            try:
                api_key = self.maps['api_key']
            except KeyError:
                raise RuntimeError('Google Maps api_key not set in the maps configuration')

            start = parse_time(http_request.args.get('start', default='yesterday'))
            end = parse_time(http_request.args.get('end', default='now'))
            zoom = http_request.args.get('zoom', default=None)

            return render_template('map.html', config=self.maps,
                                   utils=HttpUtils, start=start, end=end,
                                   zoom=zoom, token=Config.get('token'), api_key=api_key,
                                   websocket_port=self.websocket_port)

        return app


    def websocket(self):
        """ Websocket main server """
        import websockets
        set_thread_name('WebsocketServer')

        async def register_websocket(websocket, path):
            address = websocket.remote_address[0] if websocket.remote_address \
                else '<unknown client>'

            self.logger.info('New websocket connection from {}'.format(address))
            self.active_websockets.add(websocket)

            try:
                await websocket.recv()
            except websockets.exceptions.ConnectionClosed:
                self.logger.info('Websocket client {} closed connection'.format(address))
                self.active_websockets.remove(websocket)

        websocket_args = {}
        if self.ssl_context:
            websocket_args['ssl'] = self.ssl_context

        loop = get_or_create_event_loop()
        loop.run_until_complete(
            websockets.serve(register_websocket, '0.0.0.0', self.websocket_port,
                             **websocket_args))
        loop.run_forever()


    def run(self):
        super().run()
        os.putenv('FLASK_APP', 'platypush')
        os.putenv('FLASK_ENV', 'production')
        kwargs = {
            'host':'0.0.0.0', 'port':self.port, 'use_reloader':False
        }

        if self.ssl_context:
            kwargs['ssl_context'] = self.ssl_context

        self.logger.info('Initialized HTTP backend on port {}'.format(self.port))

        webserver = self.webserver()
        self.server_proc = Process(target=webserver.run,
                                   name='WebServer',
                                   kwargs=kwargs)
        self.server_proc.start()

        if not self.disable_websocket:
            self.websocket_thread = Thread(target=self.websocket)
            self.websocket_thread.start()

        self.server_proc.join()


class HttpUtils(object):
    @staticmethod
    def widget_columns_to_html_class(columns):
        if not isinstance(columns, int):
            raise RuntimeError('columns should be a number, got "{}"'.format(columns))

        if columns == 1:
            return 'one column'
        elif columns == 2:
            return 'two columns'
        elif columns == 3:
            return 'three columns'
        elif columns == 4:
            return 'four columns'
        elif columns == 5:
            return 'five columns'
        elif columns == 6:
            return 'six columns'
        elif columns == 7:
            return 'seven columns'
        elif columns == 8:
            return 'eight columns'
        elif columns == 9:
            return 'nine columns'
        elif columns == 10:
            return 'ten columns'
        elif columns == 11:
            return 'eleven columns'
        elif columns == 12:
            return 'twelve columns'
        else:
            raise RuntimeError('Constraint violation: should be 1 <= columns <= 12, ' +
                               'got columns={}'.format(columns))

    @staticmethod
    def search_directory(directory, *extensions, recursive=False):
        files = []

        if recursive:
            for root, subdirs, files in os.walk(directory):
                for file in files:
                    if not extensions or os.path.splitext(file)[1].lower() in extensions:
                        files.append(os.path.join(root, file))
        else:
            for file in os.listdir(directory):
                if not extensions or os.path.splitext(file)[1].lower() in extensions:
                    files.append(os.path.join(directory, file))

        return files

    @classmethod
    def search_web_directory(cls, directory, *extensions):
        directory = os.path.abspath(os.path.expanduser(directory))
        resource_dirs = get_backend('http').resource_dirs
        resource_path = None
        uri = ''

        for name, resource_path in resource_dirs.items():
            if directory.startswith(resource_path):
                subdir = re.sub('^{}(.*)$'.format(resource_path),
                                '\\1', directory)
                uri = '/resources/' + name
                break

        if not uri:
            raise RuntimeError('Directory {} not found among the available ' +
                               'static resources on the webserver'.format(
                                   directory))

        results = [
            re.sub('^{}(.*)$'.format(resource_path), uri + '\\1', path)
            for path in cls.search_directory(directory, *extensions)
        ]

        return results

    @classmethod
    def to_json(cls, data):
        return json.dumps(data)

    @classmethod
    def from_json(cls, data):
        return json.loads(data)


# vim:sw=4:ts=4:et:
