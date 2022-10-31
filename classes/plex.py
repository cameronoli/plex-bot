from plexapi.server import PlexServer

class plexClient():
    def __init__(self, plexUrl, plexToken):
        self.client = PlexServer(plexUrl, plexToken)
        
    def searchPlexTitles(self, section, searchString):
        searchResults = self.client.library.section(section).search(searchString)
        resultTitles = []
        messageString = "Plex Results: \n"
        for title in searchResults:
            resultTitles += [title.title]
            messageString += title.title + "\n"
        return messageString