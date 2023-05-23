import discord
from discord.ext import commands
from classes.session import NewSession
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)
_channel = bot.get_channel(895221843252887602)

@bot.event
async def on_ready():
    channel = bot.get_channel(895221843252887602)
    global _channel 
    _channel = channel
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=2, name="User Commands"))
    NewSession(channel=_channel, me=isMe, loop=bot.loop)

def isMe(m):
    return m.author == bot.user

async def changeStatus(title):
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=1, name=title)) 

def sendMessage(content=None, view=None, embed=None):
    asyncio.run_coroutine_threadsafe(sendMess(content=content, view=view, embed=embed), bot.loop)
    
async def sendMess(content=None, view=None, embed=None):
    _channel.send(content=content, view=view, embed=embed)
       
bot.run(open("/usr/src/app/secrets/bot-tokens/prod.txt").readline().strip())