from discord.ui import Modal, TextInput
class searchModal(Modal, title="What are you looking for?"):
    def __init__(self, torrentType):
        super().__init__()
        self.torrentType = torrentType
    searchInput = TextInput(label="Enter your search query:",required=True,min_length=3)
    async def on_submit(self, interaction):
        await interaction.response.send_message(search(self.torrentType, self.searchInput.value))