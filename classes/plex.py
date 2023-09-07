from plexapi.server import PlexServer

class PlexClient():
    def __init__(self, plexUrl, plexToken):
        self.client = PlexServer(plexUrl, plexToken)
        
    def searchPlexTitles(self, section, searchString):
        searchResults = self.client.library.section(section)
        for result in searchResults.search(searchString):
            print(result)
        resultTitles = []
        messageString = "Plex Results: \n"
        for title in searchResults:
            resultTitles += [title.title]
            messageString += title.title + "\n"
        return messageString