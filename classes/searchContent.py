from .plex import plexClient
from .qBitTorrent import qBit

class searchContent():
    def __init__(self):
        self.plexUrl = 'https://watch.oliverlegacy.net'
        self.plexToken = open("/home/cameron/projects/plex-bot/secrets/bot-tokens/plex.txt").readline().strip()
        self.qHost = '192.168.1.157:8080'
        self.qUsername='admin'
        self.qPassword= open("/home/cameron/projects/plex-bot/secrets/bot-tokens/qbittorrent.txt").readline().strip()


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
        pClient = plexClient(self.plexUrl, self.plexToken)
        plexTitleResults = pClient.searchPlexTitles(plexLibrary, searchString)
        print('Done with Plex', plexTitleResults)
        qClient = qBit(self.qHost, self.qUsername, self.qPassword)
        qBitTorrentResults = qClient.searchQBitTorrent(searchString, qBitTorrentPlugin, qBitTorrentLibrary)
        return "```" + plexTitleResults + "\n \n" + qBitTorrentResults + "```"
