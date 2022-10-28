from discord.ui import Modal, TextInput

class downloadModal(Modal,title="Go Ahead and Download something."):
    def __init__(self, torrentType):
        super().__init__(timeout=10)
        self.torrentType = torrentType
    torrentInput = TextInput(label="Paste your URL or Magnet link here:",required=True,min_length=10)
    async def on_submit(self):
        self.downloadTorrent(self.torrentType, self.torrentInput.value)    
    async def on_timeout(self):
        pass