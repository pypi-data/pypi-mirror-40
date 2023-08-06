import mpd
import re
import time

from platypush.plugins import action
from platypush.plugins.music import MusicPlugin

class MusicMpdPlugin(MusicPlugin):
    """
    This plugin allows you to interact with an MPD/Mopidy music server.  MPD
    (https://www.musicpd.org/) is a flexible server-side protocol/application
    for handling music collections and playing music, mostly aimed to manage
    local libraries. Mopidy (https://www.mopidy.com/) is an evolution of MPD,
    compatible with the original protocol and with support for multiple music
    sources through plugins (e.g. Spotify, TuneIn, Soundcloud, local files
    etc.).

    Requires:

        * **python-mpd2** (``pip install python-mpd2``)
    """

    def __init__(self, host, port=6600):
        """
        :param host: MPD IP/hostname
        :type host: str

        :param port: MPD port (default: 6600)
        :type port: int
        """

        super().__init__()
        self.host = host
        self.port = port
        self.client = mpd.MPDClient(use_unicode=True)
        self.client.connect(self.host, self.port)

    def _exec(self, method, *args, **kwargs):
        getattr(self.client, method)(*args, **kwargs)
        return self.status().output

    @action
    def play(self, resource=None):
        """
        Play a resource by path/URI

        :param resource: Resource path/URI
        :type resource: str
        """

        if resource:
            self.clear()
            self.add(resource)
        return self._exec('play')

    @action
    def play_pos(self, pos):
        """
        Play a track in the current playlist by position number

        :param pos: Position number
        :type resource: int
        """

        return self._exec('play', pos)

    @action
    def pause(self):
        """ Pause playback """

        status = self.status().output['state']
        if status == 'play': return self._exec('pause')
        else: return self._exec('play')

    @action
    def pause_if_playing(self):
        """ Pause playback only if it's playing """

        status = self.status().output['state']
        if status == 'play':
            return self._exec('pause')

    @action
    def play_if_paused(self):
        """ Play only if it's paused (resume) """

        status = self.status().output['state']
        if status == 'pause':
            return self._exec('play')

    @action
    def play_if_paused_or_stopped(self):
        """ Play only if it's paused or stopped """

        status = self.status().output['state']
        if status == 'pause' or status == 'stop':
            return self._exec('play')

    @action
    def stop(self):
        """ Stop playback """
        return self._exec('stop')


    @action
    def play_or_stop(self):
        """ Play or stop (play state toggle) """
        status = self.status().output['state']
        if status == 'play':
            return self._exec('stop')
        else:
            return self._exec('play')

    @action
    def playid(self, track_id):
        """
        Play a track by ID

        :param track_id: Track ID
        :type track_id: str
        """

        return self._exec('playid', track_id)

    @action
    def next(self):
        """ Play the next track """
        return self._exec('next')

    @action
    def previous(self):
        """ Play the previous track """
        return self._exec('previous')

    @action
    def setvol(self, vol):
        """
        Set the volume

        :param vol: Volume value (range: 0-100)
        :type vol: int
        """
        return self._exec('setvol', vol)

    @action
    def volup(self, delta=10):
        """
        Turn up the volume

        :param delta: Volume up delta (default: +10%)
        :type delta: int
        """

        volume = int(self.status().output['volume'])
        new_volume = min(volume+delta, 100)
        self.setvol(str(new_volume))
        return self.status()

    @action
    def voldown(self, delta=10):
        """
        Turn down the volume

        :param delta: Volume down delta (default: -10%)
        :type delta: int
        """

        volume = int(self.status().output['volume'])
        new_volume = max(volume-delta, 0)
        self.setvol(str(new_volume))
        return self.status()

    @action
    def random(self, value=None):
        """
        Set random mode

        :param value: If set, set the random state this value (true/false). Default: None (toggle current state)
        :type value: bool
        """

        if value is None:
            value = int(self.status().output['random'])
            value = 1 if value == 0 else 0
        return self._exec('random', value)

    @action
    def repeat(self, value=None):
        """
        Set repeat mode

        :param value: If set, set the repeat state this value (true/false). Default: None (toggle current state)
        :type value: bool
        """

        if value is None:
            value = int(self.status().output['repeat'])
            value = 1 if value == 0 else 0
        return self._exec('repeat', value)

    @action
    def shuffle(self):
        """
        Shuffles the current playlist
        """

        return self._exec('shuffle')

    @action
    def add(self, resource):
        """
        Add a resource (track, album, artist, folder etc.) to the current playlist

        :param resource: Resource path or URI
        :type resource: str
        """

        if isinstance(resource, list):
            for r in resource:
                r = self._parse_resource(r)
                try:
                    self._exec('add', r)
                except Exception as e:
                    self.logger.warning('Could not add {}: {}'.format(r, e))

            return self.status().output

        r = self._parse_resource(resource)
        return self._exec('add', r)

    @classmethod
    def _parse_resource(cls, resource):
        if resource and resource.startswith('spotify:playlist:'):
            # Old Spotify URI format, convert it to new
            m = re.match('^spotify:playlist:(.*)$', resource)
            resource = 'spotify:user:spotify:playlist:' + m.group(1)
        return resource

    @action
    def load(self, playlist):
        """
        Load and play a playlist by name

        :param playlist: Playlist name
        :type playlist: str
        """

        self._exec('load', playlist)
        return self.play()

    @action
    def clear(self):
        """ Clear the current playlist """
        return self._exec('clear')

    @action
    def seekcur(self, value):
        """
        Seek to the specified position

        :param value: Seek position in seconds, or delta string (e.g. '+15' or '-15') to indicate a seek relative to the current position
        :type value: int
        """

        return self._exec('seekcur', value)

    @action
    def forward(self):
        """ Go forward by 15 seconds """

        return self._exec('seekcur', '+15')

    @action
    def back(self):
        """ Go backward by 15 seconds """

        return self._exec('seekcur', '-15')

    @action
    def status(self):
        """
        :returns: The current state.

        Example response::

            output = {
                "volume": "9",
                "repeat": "0",
                "random": "0",
                "single": "0",
                "consume": "0",
                "playlist": "52",
                "playlistlength": "14",
                "xfade": "0",
                "state": "play",
                "song": "9",
                "songid": "3061",
                "nextsong": "10",
                "nextsongid": "3062",
                "time": "161:255",
                "elapsed": "161.967",
                "bitrate": "320"
            }
        """

        retries = 0
        max_retries = 2

        while retries < max_retries:
            try:
                return self.client.status()
            except Exception as e:
                self.logger.warning('Unable to parse mpd status: {}'.format(e))
                retries += 1
                time.sleep(1)

    @action
    def currentsong(self):
        """
        :returns: The currently played track.

        Example response::

            output = {
                "file": "spotify:track:7CO5ADlDN3DcR2pwlnB14P",
                "time": "255",
                "artist": "Elbow",
                "album": "Little Fictions",
                "title": "Kindling",
                "date": "2017",
                "track": "10",
                "pos": "9",
                "id": "3061",
                "albumartist": "Elbow",
                "x-albumuri": "spotify:album:6q5KhDhf9BZkoob7uAnq19"
            }
        """

        track = self.client.currentsong()
        if 'title' in track and ('artist' not in track
                                 or not track['artist']
                                 or re.search('^tunein:', track['file'])):
            m = re.match('^\s*(.+?)\s+-\s+(.*)\s*$', track['title'])
            if m and m.group(1) and m.group(2):
                track['artist'] = m.group(1)
                track['title'] = m.group(2)

        return track

    @action
    def playlistinfo(self):
        """
        :returns: The tracks in the current playlist as a list of dicts.

        Example output::

            output = [
                {
                    "file": "spotify:track:79VtgIoznishPUDWO7Kafu",
                    "time": "355",
                    "artist": "Elbow",
                    "album": "Little Fictions",
                    "title": "Trust the Sun",
                    "date": "2017",
                    "track": "3",
                    "pos": "10",
                    "id": "3062",
                    "albumartist": "Elbow",
                    "x-albumuri": "spotify:album:6q5KhDhf9BZkoob7uAnq19"
                },
                {
                    "file": "spotify:track:3EzTre0pxmoMYRuhJKMHj6",
                    "time": "219",
                    "artist": "Elbow",
                    "album": "Little Fictions",
                    "title": "Gentle Storm",
                    "date": "2017",
                    "track": "2",
                    "pos": "11",
                    "id": "3063",
                    "albumartist": "Elbow",
                    "x-albumuri": "spotify:album:6q5KhDhf9BZkoob7uAnq19"
                },
            ]
        """

        return self.client.playlistinfo()

    @action
    def listplaylists(self):
        """
        :returns: The playlists available on the server as a list of dicts.

        Example response::

            output = [
                {
                    "playlist": "Rock",
                    "last-modified": "2018-06-25T21:28:19Z"
                },
                {
                    "playlist": "Jazz",
                    "last-modified": "2018-06-24T22:28:29Z"
                },
                {
                    # ...
                }
            ]
        """

        return sorted(self.client.listplaylists(), key=lambda p: p['playlist'])

    @action
    def lsinfo(self, uri=None):
        """
        Returns the list of playlists and directories on the server
        """

        output = self.client.lsinfo(uri) if uri else self.client.lsinfo()
        return output

    @action
    def plchanges(self, version):
        """
        Show what has changed on the current playlist since a specified playlist
        version number.

        :param version: Version number
        :type version: int

        :returns: A list of dicts representing the songs being added since the specified version
        """

        return self.client.plchanges(version)

    @action
    def searchaddplaylist(self, name):
        """
        Search and add a playlist by (partial or full) name

        :param name: Playlist name, can be partial
        :type name: str
        """

        playlists = list(map(lambda _: _['playlist'],
                        filter(lambda playlist:
                               name.lower() in playlist['playlist'].lower(),
                               self.client.listplaylists())))

        if len(playlists):
            self.client.clear()
            self.client.load(playlists[0])
            self.client.play()
            return {'playlist': playlists[0]}

    @action
    def find(self, filter, *args, **kwargs):
        """
        Find in the database/library by filter.

        :param filter: Search filter. MPD treats it as a key-valued list (e.g. ``["artist", "Led Zeppelin", "album", "IV"]``)
        :type filter: list[str]
        :returns: list[dict]
        """

        return self.client.find(*filter, *args, **kwargs)

    @action
    def findadd(self, filter, *args, **kwargs):
        """
        Find in the database/library by filter and add to the current playlist.

        :param filter: Search filter. MPD treats it as a key-valued list (e.g. ``["artist", "Led Zeppelin", "album", "IV"]``)
        :type filter: list[str]
        :returns: list[dict]
        """

        return self.client.findadd(*filter, *args, **kwargs)

    @action
    def search(self, filter, *args, **kwargs):
        """
        Free search by filter.

        :param filter: Search filter. MPD treats it as a key-valued list (e.g. ``["artist", "Led Zeppelin", "album", "IV"]``)
        :type filter: list[str]
        :returns: list[dict]
        """

        items = self.client.search(*filter, *args, **kwargs)

        # Spotify results first
        items = sorted(items, key=lambda item:
                       0 if item['file'].startswith('spotify:') else 1)

        return items

    @action
    def searchadd(self, filter, *args, **kwargs):
        """
        Free search by filter and add the results to the current playlist.

        :param filter: Search filter. MPD treats it as a key-valued list (e.g. ``["artist", "Led Zeppelin", "album", "IV"]``)
        :type filter: list[str]
        :returns: list[dict]
        """

        return self.client.searchadd(*filter, *args, **kwargs)

# vim:sw=4:ts=4:et:

