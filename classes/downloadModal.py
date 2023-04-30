from discord.ui import Modal, TextInput
from .qBitTorrent import Qbit
from classes.sendUserMessage import SendUserMessage

class DownloadModal(Modal,title="Go Ahead and Download something."):
    def __init__(self, torrentType, loop):
        super().__init__(timeout=10)
        self.torrentType = torrentType
        self.loop = loop

    torrentInput = TextInput(label="Paste your URL or Magnet link here:",required=True,min_length=10)
    async def on_submit(self, interaction):
        qClient = Qbit()
        qClient.downloadTorrent(self.torrentType, self.torrentInput.value, interaction.user)
        await interaction.response.defer()
        await SendUserMessage(interaction=interaction, loop=self.loop).generateMessage()
    async def on_timeout(self, interaction):
        await interaction.response.defer()