from email import message
from plexapi.server import PlexServer
import discord
from discord.ui import Button, View, Modal, TextInput, Select
from discord.ext import commands
import qbittorrentapi
import time

<<<<<<< Updated upstream
qbt_client = qbittorrentapi.Client(host='192.168.1.157:8080', username='admin', password= open("/home/cameron/projects/plex-bot/secrets/bot-tokens/qbittorrent.txt").readline().strip())
=======
'''print("Logging in...")

qbt_client = qbittorrentapi.Client(host='192.168.1.20:8080', username='admin', password='adminadmin')
>>>>>>> Stashed changes
try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)
print("Logged in.")

<<<<<<< Updated upstream
plexUrl = 'https://watch.oliverlegacy.net'
plexToken = open("/home/cameron/projects/plex-bot/secrets/bot-tokens/plex.txt").readline().strip()
plex = PlexServer(plexUrl, plexToken)
=======
print("Connecting to db...")
db = psycopg2.connect(database="postgres", user="postgres", password="mysecretpassword", host="172.17.0.2", port="5432")
print("Connected to db.")
cur = db.cursor()'''


#------------------------------------------------------------------------------------------------------

#version = qbt_client.app.version
torrent_added = "Wohoo! You've just started the download for your file. use !info to check the status of in-progress torrents."
invalid_cat = " is not a valid category. Please use 'movie' or 'tv'."
invalid_link = "The URL/magnet you provided is not valid. Please find another."

bot = commands.Bot(command_prefix='$', help_command=None) #make sure to set this to the correct symbol
_ctx = None
help_file = '```This is a bot for adding movies or T.V shows to the Plex media server "Beauty" \n \
\n \
Bot Commands \n \
- $address; Returns the URL of the Plex server \n \
- $dl, $download type link \n \
    - [type]; Use "movie" when downloading a movie or "tv" when downloading a T.V show \n \
    - [link]; You must use either a magnet link or a Url to a torrent file \n \
        E.G. - Magnet: magnet:?xt=urn:btih:f5caf1161cbe9312511cf1c35a75c744e7eb8e67&dn=Survivor.S41E02.1080p%5D \n \
             - Url: https://rarbg.to/download.php?id=mhy6u3a&h=f5c&f=Survivor.S41E02.1080p.AMZN.WEBRip.DDP5.1.x264-KiNGS%5Brartv%5D-[rarbg.to].torrent \n \
- $h, $help; Returns this message \n \
- $ping; Returns "Pong!" \n \
- $search type query \n \
    - [type]; Use "movie" when searching for a movie or "tv" when searching for a T.V show \n \
    - [query]; Enter whatever you are searching for \n \
- $v; Returns the installed version of qbittorrent API \n \
```'

@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    global _ctx 
    _ctx = ctx

@bot.command()
async def address(ctx):
    await ctx.send('```http://watch.oliverlegacy.net```')
    global _ctx 
    _ctx = ctx

@bot.command()
async def help(ctx):
    await ctx.send(help_file)
    global _ctx 
    _ctx = ctx

@bot.command()
async def h(ctx):
    await help(ctx)
    global _ctx 
    _ctx = ctx

@bot.command()
async def download(ctx, cat, link):
    global _ctx 
    _ctx = ctx
    m = await get_latest_message()
    convoid = create_conversation(m.author.id)
    time.sleep(1)
    await record_message(convoid)
    if cat != "movie" and cat != "tv":
        await ctx.send(cat + invalid_cat)
        return
    try:
        response = _download(urls=link,category=cat)
        if response == "Ok.":
            time.sleep(3)
            await create_progress_card()
            delete_messages(convoid)
            return True
        else:
            await ctx.send(invalid_link)
            return False
    except Exception as e: 
         print(e)

def _download(urls, category):
        return qbt_client.torrents_add(urls=urls,category=category)

@bot.command()
async def dl(ctx, cat, link):
    await download(ctx, cat, link)

@bot.command()
async def v(ctx):
    await ctx.send(version)

@bot.command()  
async def search(ctx, plug, *pat):
    global _ctx 
    _ctx = ctx
    m = await get_latest_message()
    convoid = create_conversation(m.author.id)
    await record_message(convoid)
    pattern = " ".join(pat)
>>>>>>> Stashed changes

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
        await interaction.response.send_modal(searchModal())
    async def downloadTvButtonCallback(interaction):
        await interaction.response.send_modal(downloadModal())
    async def searchMovieButtonCallback(interaction):
        await interaction.response.send_modal(searchModal())
    async def downloadMovieButtonCallback(interaction):
        await interaction.response.send_modal(downloadModal())
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

class downloadModal(Modal,title="Go Ahead and Download something."):
    urlInput = TextInput(label="If you have a URL, paste it here:",required=False,min_length=3)
    magnetInput = TextInput(label="If you have a magnet, paste it here:",required=False,min_length=5)
    async def on_submit(self, interaction):
        if self.urlInput.value != "":
            await interaction.response.send_message(self.urlInput.value)
        elif self.magnetInput.value != "":
            await interaction.response.send_message(self.magnetInput.value)
        else:
            await interaction.response.send_message("Mate, you gotta enter something")
        await newSession()
               
class searchModal(Modal, title="What are you looking for?"):
    searchInput = TextInput(label="Enter your search query:",required=True,min_length=3)
    async def on_submit(self, interaction):
        await newSession()
        await interaction.response.send_message(self.searchInput.value)
        

@bot.command()  #searches plex titles
async def search(library, *searchString):
    searchString = " ".join(searchString)
    plexLibrary = ""
    if library == "movie":
        plexLibrary = "Movies"
        qBitTorrentPlugin = "YTS"
    elif library == "tv":
        plexLibrary = "TV Shows"
        qBitTorrentPlugin = "RARBG"
    plexTitleResults = searchPlexTitles(plexLibrary, searchString)
    qBitTorrentResults = searchQBitTorrent(searchString, qBitTorrentPlugin, library)
    return plexTitleResults + "\n \n " + qBitTorrentResults

def searchPlexTitles(section, searchString):
    searchResults = plex.library.section(section).search(searchString)
    resultTitles = []
    messageString = "Plex Results: \n"
    for title in searchResults:
        resultTitles += [title.title]
        messageString += title.title + "\n"
    return messageString

def searchQBitTorrent(searchString, plugin, category):
    return "qBitTorrent Results: \n Nothing Yet!"
        
bot.run(open("/home/cameron/projects/plex-bot/secrets/bot-tokens/dev.txt").readline().strip())


