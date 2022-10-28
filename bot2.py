from classes.searchModal import searchModal
from classes.downloadModal import downloadModal
from plexapi.server import PlexServer
import discord
from discord.ui import Button, View, Modal, TextInput, Select
from discord.ext import commands
import qbittorrentapi
import time

qbit = qbittorrentapi.Client(host='192.168.1.157:8080', username='admin', password= open("/home/cameron/projects/plex-bot/secrets/bot-tokens/qbittorrent.txt").readline().strip())
try:
    qbit.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)
print("Logged in.")

plexUrl = 'https://watch.oliverlegacy.net'
plexToken = open("/home/cameron/projects/plex-bot/secrets/bot-tokens/plex.txt").readline().strip()
plex = PlexServer(plexUrl, plexToken)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)
_channel = bot.get_channel(904528686789828648)

@bot.event
async def on_ready():
    channel = bot.get_channel(904528686789828648)
    global _channel 
    _channel = channel
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=2, name="User Commands"))
    await newSession()

def isMe(m):
    return m.author == bot.user

async def changeStatus(title):
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=1, name=title))

async def newSession():
    await _channel.purge(limit=3, check=isMe)
    time.sleep(3)
    await sendMessage(content="Smiley Day to you! \n I'm plex-bot, How can I help you today?",view=initialButtons())        

async def sendMessage(content=None, view=None, embed=None):
    await _channel.send(content=content, view=view, embed=embed)
    
def initialButtons():
    searchTvButton = Button(label="Search TV Shows",style=discord.ButtonStyle.primary, custom_id="searchTvButton")
    searchMovieButton = Button(label="Search Movies",style=discord.ButtonStyle.primary, custom_id="searchMovieButton")
    downloadTvButton = Button(label="Download TV Show",style=discord.ButtonStyle.primary, custom_id="downloadTvButton")
    downloadMovieButton = Button(label="Download Movie",style=discord.ButtonStyle.primary, custom_id="downloadMovieButton")
    helpButton = Button(label="Help",style=discord.ButtonStyle.primary, custom_id="helpButton")
    view = View()
    view.add_item(searchTvButton)
    view.add_item(searchMovieButton)
    view.add_item(downloadTvButton)
    view.add_item(downloadMovieButton)
    view.add_item(helpButton)
    
    
    async def searchTvButtonCallback(interaction):
        await interaction.response.send_modal(searchModal("tv"))
    async def downloadTvButtonCallback(interaction):
        await interaction.response.send_modal(downloadModal("tv"))
    async def searchMovieButtonCallback(interaction):
        await interaction.response.send_modal(searchModal("movie"))
    async def downloadMovieButtonCallback(interaction):
        await interaction.response.send_modal(downloadModal("movie"))
    async def helpButtonCallback(interaction):
        message, helpView = helpMessage()
        await interaction.response.send_message(message, view=helpView) 
    
    searchTvButton.callback = searchTvButtonCallback
    searchMovieButton.callback = searchMovieButtonCallback
    downloadMovieButton.callback = downloadMovieButtonCallback
    downloadTvButton.callback = downloadTvButtonCallback
    helpButton.callback = helpButtonCallback
    return(view)

def helpMessage():
    view =View()
    doneButton = Button(label="Done, Thanks!", style=discord.ButtonStyle.primary, custom_id="doneButton")
    view.add_item(doneButton)
    async def doneButtonCallback(iteraction):
        await newSession()
    doneButton.callback = doneButtonCallback
    helpString = "```This is the v2 bot for adding movies or T.V shows to Cameron's Plex media server, Beauty. \n \n \
To download something: \n \
    1. Select the 'Download' button, \n \
    2. Paste either a magnet link OR Url to a torrent file (examples below) \n \
    3. From the dropdown, select the appropriate torrent type (movie/tv show) \n \
    4. Submit \n \n \
E.G. - Magnet: magnet:?xt=urn:btih:f5caf1161cbe9312511cf1c35a75c744e7eb8e67&dn=Survivor.S41E02.1080p%5D \n \
     - Url: https://rarbg.to/download.php?id=mhy6u3a&h=f5c&f=Survivor.S41E02.1080p.AMZN.WEBRip.DDP5.1.x264-KiNGS%5Brartv%5D-[rarbg.to].torrent \n \
- $info; Returns info on all in-progress torrents \n \
```"
    return helpString, view


               
        
def search(library, *searchString):
    searchString = " ".join(searchString)
    plexLibrary = ""
    if library == "movie":
        plexLibrary = "Movies"
        qBitTorrentPlugin = "YTS"
        qBitTorrentLibrary = "all"
    elif library == "tv":
        plexLibrary = "TV Shows"
        qBitTorrentPlugin = "RARBG"
        qBitTorrentLibrary = "tv"
    plexTitleResults = searchPlexTitles(plexLibrary, searchString)
    qBitTorrentResults = searchQBitTorrent(searchString, qBitTorrentPlugin, qBitTorrentLibrary)
    return "'''" + plexTitleResults + "\n \n " + qBitTorrentResults + "'''"

def searchPlexTitles(section, searchString):
    searchResults = plex.library.section(section).search(searchString)
    resultTitles = []
    messageString = "Plex Results: \n"
    for title in searchResults:
        resultTitles += [title.title]
        messageString += title.title + "\n"
    print(messageString)
    return messageString

def searchQBitTorrent(searchString, plugin, category):
    searchJob = qbit.search.start(searchString, plugin, category)
    searchId = searchJob.get("id")
    while qbit.search.status()[0].get("total") < 10: #limits results to 10
        time.sleep(0.5)
    qbit.search.stop(searchId)
    resultsJson = qbit.search.results(searchId, 10, 0) #limits results to 10
    searchResultsList = resultsJson.get("results")
    resultDict = dict((r.get("fileName"), r.get("fileUrl")) for r in searchResultsList)
    resultString =""
    for resultDictKey in resultDict.keys():
        resultString += str(resultDict.keys().index(resultDictKey) +1) + resultDictKey + "\n" 
    return resultString
    #maybe instead, have the qbittorrent results display in a drop-down so users can select the torrent to download?

def downloadTorrent(torrentType, torrentLink):
    try:
        qbit.torrents.add(urls=torrentLink, category=torrentType)
    except Exception as e: 
         print(e)
    
bot.run(open("/home/cameron/projects/plex-bot/secrets/bot-tokens/dev.txt").readline().strip())


