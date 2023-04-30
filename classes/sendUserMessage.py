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
            await asyncio.sleep(20)
            torrentName = self.qClient.getTorrents(tag=self.interaction.user)
        message = "Hey There! \n I just wanted to let you know that the torrent listed below has completed downloading and is now available on the Plex server. \n \n" + torrentName
        await self.interaction.user.send(content=message)
