from discord.ui import Modal, TextInput
from .searchContent import searchContent
import asyncio
class searchModal(Modal, title="What are you looking for?"):
    def __init__(self, torrentType):
        super().__init__(timeout=7)
        self.torrentType = torrentType
        self.search = searchContent()
    searchInput = TextInput(label="Enter your search query:",required=True,min_length=3)
    async def on_submit(self, interaction):
        #need to save the lsit of results from qbit to a list[] for the drop-down view \
        #attach the view to the message in response to be selected.
        #await interaction.response.send_message("Searching...")
        #await interaction.response.edit_message(content=self.search.search(self.torrentType, self.searchInput.value))
        await interaction.response.defer()
        await interaction.followup.send(self.search.search(self.torrentType, self.searchInput.value))