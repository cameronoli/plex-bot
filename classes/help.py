class Help():
    def __init__(self, loop, channel, me) -> None:
        self.loop = loop
        self.channel = channel
        self.me = me

    def helpMessage(self):
        helpString = "```This is the v2 bot for adding movies or T.V shows to Cameron's Plex media server, Beauty. \n \n \
To download something: \n \
    1. Select the appropriate'Download' button, \n \
    2. Paste either a magnet link OR Url to a torrent file (examples below) \n \
    3. Submit \n \n \
E.G. \n \
    - Magnet: magnet:?xt=urn:btih:f5caf1161cbe9312511cf1c35a75c744e7eb8e67&dn=Survivor.S41E02.1080p%5D \n \n \
    - Url: https://rarbg.to/download.php?id=mhy6u3a&h=f5c&f=Survivor.S41E02.1080p.AMZN.WEBRip.DDP5.1.x264-KiNGS%5Brartv%5D-[rarbg.to].torrent \n \n \
You'll recieve a message from the bot when the torrent is compelte. \n \
    ```"
        return helpString
