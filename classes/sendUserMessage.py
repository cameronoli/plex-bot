from classes.qBitTorrent import Qbit
import asyncio
import time

class SendUserMessage():
    def __init__(self, interaction, loop) -> None:
        self.interaction = interaction
        self.loop = loop
        self.qClient = Qbit()
        
    async def generateMessage(self) -> None:
        torrentName = ""
        while torrentName == "":
            await asyncio.sleep(10)
            torrentName = self.qClient.getTorrents(tag=self.interaction.user)
            print("No Torrents just yet. Retrying..")
        print("Torrents:", torrentName)
        message = f"Hey {self.interaction.user.mention}! \n I just wanted to let you know that the torrent listed below has completed downloading and is now available on the Plex server. \n \n" + torrentName
        await self.interaction.user.send(content=message)

    async def generateErrorMessage(self) -> None:
        message = f"Hey {self.interaction.user.mention}! \n Seems like there was something wrong with the torrent link/URL you provided. \n Can you try again or find another torrent link? Thanks!"
        await self.interaction.user.send(content=message)