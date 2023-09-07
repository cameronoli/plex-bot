from  qbittorrentapi import Client, LoginFailed
import time

class Qbit():
    def __init__(self, 
                 host='tasks.torrent:8080', 
                 username='admin', 
                 password=open("/usr/src/app/secrets/bot-tokens/qbittorrent.txt").readline().strip()):
        self.client = Client(host=host, username=username, password=password)
        try:
            self.client.auth_log_in()
        except LoginFailed as e:
            print(e)
        print("Logged in.")
        
    def searchQBitTorrent(self,searchString, plugin, category) -> str:
        searchJob = self.client.search.start(searchString, plugin, category)
        searchId = searchJob.get("id")
        timer = 1
        while (self.client.search.status(searchId)[0].get("total") < 10) and (timer < 10): #limits results to 10
            time.sleep(0.5)
            timer += 1
        self.client.search.stop(searchId)
        resultsJson = self.client.search.results(searchId, 10, 0) #limits results to 10
        searchResultsList = resultsJson.get("results")
        resultDict = dict((r.get("fileName"), r.get("fileUrl")) for r in searchResultsList)
        resultString ="QBitTorrent Results: \n"
        for resultDictKey in resultDict.keys():
            resultString += resultDictKey + "\n" 
        return resultString
        #maybe instead, have the qbittorrent results display in a drop-down so users can select the torrent to download?
        
    def downloadTorrent(self,torrentType, torrentLink, user) -> str:
        try:
            response = self.client.torrents.add(urls=torrentLink, category=torrentType, tags=user)
        except Exception as e: 
            print("Exception: ", e)
        print("Trying to download torrent: ", response)
        return response
            
    def getTorrents(self, filter=None, tag=None) -> str:
            inProgressTorrentList = self.client.torrents_info(status_filter=filter, tag=tag)
            returnString = "Current Torrents: \n \n"
            if len(inProgressTorrentList) > 0:
                for inProgressTorrent in inProgressTorrentList:
                    if tag != None:
                        if inProgressTorrent.get("state") == "pausedUP":
                            resultHash = inProgressTorrent.get("hash")
                            self.client.torrents_remove_tags(tags=tag, torrent_hashes=resultHash)
                            return inProgressTorrent.get("name")
                        else:
                            return ""
                    returnString += inProgressTorrent.get("name") + "\n"
                    returnString += str(round(inProgressTorrent.get("progress") * 100, 2)) + " %" + "\n \n"
            else:
                returnString = "There are no torrents currently downloading."
            return(returnString)
               
    def getSubmittedTorrent(self, hash) -> str:
        submittedTorrentList = self.client.torrents_info(torrent_hashes=hash)
        for submittedTorrent in submittedTorrentList:
            torrentName = submittedTorrent.get("name")
        return torrentName