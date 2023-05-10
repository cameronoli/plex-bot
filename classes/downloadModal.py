from discord.ui import Modal, TextInput
from .qBitTorrent import Qbit
from classes.sendUserMessage import SendUserMessage

class DownloadModal(Modal,title="Go Ahead and Download something."):
    def __init__(self, torrentType, loop) -> None:
        super().__init__(timeout=10)
        self.torrentType = torrentType
        self.loop = loop

    torrentInput = TextInput(label="Paste your URL or Magnet link here:",required=True,min_length=10)
    async def on_submit(self, interaction) -> None:
        qClient = Qbit()
        response = qClient.downloadTorrent(self.torrentType, self.torrentInput.value, interaction.user)
        await interaction.response.defer()
        if response == "Fails.":
            await SendUserMessage(interaction=interaction, loop=self.loop).generateErrorMessage()
        else:
            await SendUserMessage(interaction=interaction, loop=self.loop).generateMessage()
    async def on_timeout(self, interaction) -> None:
        await interaction.response.defer()