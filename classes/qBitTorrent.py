from  qbittorrentapi import Client, LoginFailed
import time

class qBit():
    def __init__(self, host:str, username:str, password:str):
        self.client = Client(host=host, username=username, password=password)
        try:
            self.client.auth_log_in()
        except LoginFailed as e:
            print(e)
        print("Logged in.")
        
    def searchQBitTorrent(self,searchString, plugin, category):
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
        
    def downloadTorrent(self,torrentType, torrentLink):
        try:
            self.client.torrents.add(urls=torrentLink, category=torrentType)
        except Exception as e: 
            print(e)