import discord
from discord.ext import commands
import qbittorrentapi

qbt_client = qbittorrentapi.Client(host='tasks.torrent:8080', username='admin', password='adminadmin')
try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)

version = qbt_client.app.version
torrent_added = "Wohoo! You've just started the download for your file. Check Plex shortly to watch!"
invalid_cat = "Is not a valid category. Please use 'movie' or 'tv'."
invalid_link = "The URL/magnet you provided is not valid. Please find another."

bot = commands.Bot(command_prefix='$', help_command=None)
help_file = '```This is a bot for adding movies or T.V shows to the Plex media server "Beauty" \n \
\n \
Bot Commands \n \
- $h, $help; Returns this message    \n \
- $ping; Returns "Pong!" \n \
- $dl, $download type link \n \
    - [type]; Use "movie" when downloading a movie or "tv" when downloading a T.V show \n \
    - [link]; You must use either a magnet link or a Url to a torrent file \n \
        E.G. - Magnet: magnet:?xt=urn:btih:f5caf1161cbe9312511cf1c35a75c744e7eb8e67&dn=Survivor.S41E02.1080p%5D \n \
             - Url: https://rarbg.to/download.php?id=mhy6u3a&h=f5c&f=Survivor.S41E02.1080p.AMZN.WEBRip.DDP5.1.x264-KiNGS%5Brartv%5D-[rarbg.to].torrent \n \
- $v; Returns the installed version of qbittorrent API\n \
```'

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def help(ctx):
    await ctx.send(help_file)

@bot.command()
async def h(ctx):
    await ctx.send(help_file)

@bot.command()
async def download(ctx, cat, link):
    if cat != "movie" and cat != "tv":
        await ctx.send(cat, invalid_cat)
        return
    try:
        qbt_client.torrents_add(urls=link,category=cat)
        await ctx.send(torrent_added)
    except qbittorrentapi.UnsupportedMediaType415Error as e:
        print(e)
        await ctx.send(invalid_link)
    except Exception as e: 
        print(e)
    

@bot.command()
async def dl(ctx, cat, link):
    download(ctx, cat, link)

@bot.command()
async def v(ctx):
    await ctx.send(version)

bot.run(open("secrets/bot-tokens/dev.txt").readline().strip())