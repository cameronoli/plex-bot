from .plex import PlexClient
from .qBitTorrent import Qbit

class SearchContent():
    def __init__(self):
        self.plexUrl = 'https://watch.oliverlegacy.net'
        self.plexToken = open("/home/cameron/projects/plex-bot/secrets/bot-tokens/plex.txt").readline().strip()

    def search(self,library, *searchString):
        searchString = " ".join(searchString)
        plexLibrary = ""
        if library == "movie":
            plexLibrary = "Movies"
            qBitTorrentPlugin = "YTS"
            qBitTorrentLibrary = "all"
        elif library == "tv":
            plexLibrary = "TV Shows"
            qBitTorrentPlugin = "RARBG"
            qBitTorrentLibrary = "tv"
        pClient = PlexClient(self.plexUrl, self.plexToken)
        plexTitleResults = pClient.searchPlexTitles(plexLibrary, searchString)
        print('Done with Plex', plexTitleResults)
        qClient = Qbit()
        qBitTorrentResults = qClient.searchQBitTorrent(searchString, qBitTorrentPlugin, qBitTorrentLibrary)
        return "```" + plexTitleResults + "\n \n" + qBitTorrentResults + "```"
