import time
from datetime import datetime
import asyncio
from classes.initialButtons import InitialButtons

class NewSession():
    def __init__(self, channel, me, loop):
        self.channel = channel
        self.me = me
        self.loop = loop
        self.buttons = InitialButtons(self.loop, self.channel, self.me).generateButtons()
        self.purge()
        time.sleep(5)
        self.printWelcome()
        
    def purge(self):
        asyncio.run_coroutine_threadsafe(self.channel.purge(limit=5, before=datetime.now(), check=self.me), self.loop)
        
    def printWelcome(self):
        asyncio.run_coroutine_threadsafe(self.channel.send(content="Smiley Day to you! \n I'm plex-bot, How can I help you today?", view=self.buttons), self.loop)
        
          