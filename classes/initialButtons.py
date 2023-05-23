from discord.ui import Button, View
from classes.searchModal import SearchModal
from classes.downloadModal import DownloadModal
import discord
from classes.help import Help
import asyncio
from classes.qBitTorrent import Qbit

class InitialButtons():
    def __init__(self, loop, channel, me) -> None:
        self.loop=loop
        self.channel = channel
        self.me = me
        
    
    def generateButtons(self) -> View:
        searchTvButton = Button(label="Search TV Shows",style=discord.ButtonStyle.primary, custom_id="searchTvButton")
        searchMovieButton = Button(label="Search Movies",style=discord.ButtonStyle.primary, custom_id="searchMovieButton")
        downloadTvButton = Button(label="Download TV Show",style=discord.ButtonStyle.primary, custom_id="downloadTvButton")
        downloadMovieButton = Button(label="Download Movie",style=discord.ButtonStyle.primary, custom_id="downloadMovieButton")
        helpButton = Button(label="Help",style=discord.ButtonStyle.primary, custom_id="helpButton")
        currentTorrentsButton = Button(label="Currently Downloading",style=discord.ButtonStyle.primary, custom_id="currentTorrentsButton")
        view = View(timeout=2592000.0)
        #view.add_item(searchTvButton)
        #view.add_item(searchMovieButton)
        view.add_item(downloadTvButton)
        view.add_item(downloadMovieButton)
        view.add_item(helpButton)
        view.add_item(currentTorrentsButton)
        
        
        async def searchTvButtonCallback(interaction):
            await interaction.response.send_modal(SearchModal("tv"))
        async def downloadTvButtonCallback(interaction):
            asyncio.run_coroutine_threadsafe(interaction.response.send_modal(DownloadModal("tv", loop=self.loop)), self.loop)
        async def searchMovieButtonCallback(interaction):
            await interaction.response.send_modal(SearchModal("movie"))
        async def downloadMovieButtonCallback(interaction):
            asyncio.run_coroutine_threadsafe(interaction.response.send_modal(DownloadModal("movie", loop=self.loop)), self.loop)
        async def helpButtonCallback(interaction):
            message = Help(self.loop, self.channel, self.me).helpMessage()
            await interaction.response.send_message(message, view=self.doneButton()) 
        async def currentTorrentsButtonCallback(interaction):
            await interaction.response.send_message(Qbit().getTorrents(filter="downloading"), view=self.doneButton())
        
        searchTvButton.callback = searchTvButtonCallback
        searchMovieButton.callback = searchMovieButtonCallback
        downloadMovieButton.callback = downloadMovieButtonCallback
        downloadTvButton.callback = downloadTvButtonCallback
        helpButton.callback = helpButtonCallback
        currentTorrentsButton.callback = currentTorrentsButtonCallback
        return(view)
    
    def doneButton(self) -> View:
        view =View()
        doneButton = Button(label="Done, Thanks!", style=discord.ButtonStyle.primary, custom_id="doneButton")
        view.add_item(doneButton)
        async def doneButtonCallback(iteraction):
            asyncio.run_coroutine_threadsafe(self.channel.purge(limit=1, check=self.me), self.loop)
        doneButton.callback = doneButtonCallback
        return view