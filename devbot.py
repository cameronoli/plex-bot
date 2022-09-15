from os import name
#from turtle import down
import discord
from discord.ext import commands
import qbittorrentapi
import attrdict
import json
import time
import psycopg2

print("Logging in...")

qbt_client = qbittorrentapi.Client(host='192.168.1.20:8080', username='admin', password='adminadmin')
try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)

print("Logged in.")

print("Connecting to db...")
db = psycopg2.connect(database="postgres", user="postgres", password="mysecretpassword", host="172.17.0.2", port="5432")
print("Connected to db.")
cur = db.cursor()


#------------------------------------------------------------------------------------------------------

version = qbt_client.app.version
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

    if plug == "movie":
        plugin = "YTS"
        cat = "all"
    elif plug == "tv":
        plugin = "RARBG"
        cat = "tv"
    else:
        await ctx.send("```That is not a valid category. Please use 'movie' or 'tv'.```")
        time.sleep(2)
        await record_message(9999)
        return

    await ctx.send("```Searching...```")
    time.sleep(0.5)
    await record_message(convoid)
    search_job = qbt_client.search.start(pattern, plugin, cat)
    search_id = search_job.get("id")
    linkquery = "INSERT INTO searchlink (searchid, convoid, type) VALUES (%s, %s, %s);"
    linkvalues = [search_id, convoid, plug]
    cur.execute(linkquery, linkvalues)
    db.commit()
    timer = 0
    while qbt_client.search.status()[0].get("total") < 10 & timer < 10: #limits results to 10
        time.sleep(0.5)
        timer += 1
    qbt_client.search.stop(search_id)
    results_json = qbt_client.search.results(search_id, 10, 0) #limits results to 10
    search_results = results_json.get("results")

    count = 1
    result_query = '''INSERT INTO results (resultID, searchID, fileName, fileURL) VALUES'''
    result_dict = {}
    for r in search_results:      
        result_query += ''' (%({0}count'''.format(count) + ''')s, %({0}search_id'''.format(count) + ''')s, %({0}fileName'''.format(count) + ''')s, %({0}fileUrl'''.format(count) + ''')s)'''
        result_dict.update({"{0}count".format(count): count, "{0}search_id".format(count): search_id, "{0}fileName".format(count): r.get("fileName"), "{0}fileUrl".format(count):r.get("fileUrl")})
        if count < 10:
            result_query += ''','''
        count += 1
    result_query += ";"
    cur.execute(result_query, result_dict)
    db.commit()

    await ctx.send(get_search_card(search_id))
    time.sleep(1)
    await record_message(convoid)
    last_mess = await get_latest_message()
    search_reacts = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    for react in search_reacts:
        await last_mess.add_reaction(react)
    qbt_client.search.delete(search_id)
    #save selection to completed torrent table - to be done in another method

@bot.event
async def on_reaction_add(reaction, user):
    if user.id == 904917396035362828:
        return
    query = "SELECT convoid FROM messages WHERE messageid = %s;"
    cur.execute(query, [reaction.message.id])
    convoid = cur.fetchone()[0]
    query = "SELECT messageid FROM messages WHERE convoid = %s;"
    cur.execute(query, [convoid])
    messages = cur.fetchall()
    mlist = []
    for m in messages:
        mlist += [m][0]
    query = "SELECT starter FROM conversations WHERE convo_id = %s;"
    cur.execute(query, [convoid])
    req = cur.fetchone()[0]
    if reaction.message.id in mlist and user.id == req:
        selection = get_number_for_react(reaction.emoji)
        await process_search(selection, user.id, reaction.message.id, convoid)   
    return reaction, user.id

async def process_search(selection, userid, messageid, convoid):
    #for the future - implement: if selection in range (10), do the below. else it won't be a download, perhaps add a cancel option
    query = "SELECT searchid FROM searchlink WHERE convoid = %s;"
    cur.execute(query, [convoid])
    searchid = cur.fetchone()[0]
    query = "SELECT fileurl FROM results WHERE resultid = %s AND searchid = %s;"
    qvalues = [selection, searchid]
    cur.execute(query, qvalues)
    url = cur.fetchone()[0]
    query = "SELECT filename FROM results WHERE resultid = %s AND searchid = %s;"
    qvalues = [selection, searchid]
    cur.execute(query, qvalues)
    filename = cur.fetchone()[0]
    query = "SELECT type FROM searchlink WHERE searchid = %s;"
    cur.execute(query, [searchid])
    category = cur.fetchone()[0]
    if _download(url, category):
        time.sleep(5)
        await delete_messages(convoid)
        time.sleep(3)
        await create_progress_card()
        time.sleep(2)
        await record_message(convoid)
        await clear_results(searchid)

async def create_progress_card():
    global _ctx
    ctx = _ctx
    downloading_torrents = qbt_client.torrents_info("downloading")
    if downloading_torrents == []:
        await ctx.send("```There are no torrents currently downloading.```")
        time.sleep(2)
        await record_message(9999)
        time.sleep(10)
        await delete_messages(9999)
    else:
        for torrent in downloading_torrents:
            torrent_name = torrent.get("name")
            torrent_progress = round(torrent.get("progress") * 100, 2)
            progress_bar = progressBar(torrent_progress, torrent_name)
            await ctx.send(progress_bar)
            time.sleep(2)
            await record_message(9999)
        await update_progress_card()

async def update_progress_card():
    time.sleep(10)
    await delete_messages()
    time.sleep(3)
    await create_progress_card()

async def clear_results(searchid):
    query = "DELETE FROM results WHERE searchid = %s;"
    cur.execute(query, [searchid])
    db.commit()

async def end_conversation(convoid):
    query = "DELETE FROM conversations WHERE convo_id = %s;"
    cur.execute(query, [convoid])
    db.commit()

async def delete_messages(convoid=None):
    global _ctx
    ctx = _ctx
    if convoid == None:
        query = "SELECT messageid FROM messages;"
    else:
        query = "SELECT messageid FROM messages WHERE convoid = %s;"
    cur.execute(query, [convoid])
    db.commit()
    results = cur.fetchall()
    for id in results:
        try:
            to_delete = await get_message(id[0])
            time.sleep(1)
            await to_delete.delete()
            time.sleep (5)
        except discord.errors.NotFound as e:
            print(e)
    if convoid == None:
        query = "DELETE FROM messages;"
    else:
        query = "DELETE FROM messages WHERE convoid = %s;"
        await end_conversation(convoid)
    cur.execute(query, [convoid])
    db.commit()

def get_number_for_react(react):
    react_dict = {"1️⃣":1, "2️⃣":2, "3️⃣":3, "4️⃣":4, "5️⃣":5, "6️⃣":6, "7️⃣":7, "8️⃣":8, "9️⃣":9, "🔟":10}
    return react_dict.get(react)

async def get_message(messageid):
    channel = bot.get_channel(904528686789828648) #this is the channel ID
    message = await channel.fetch_message(messageid)
    return message

async def get_latest_message(): #gets latest message in the channel (in this case #general in dev server)
    channel = bot.get_channel(904528686789828648) #this is the channel ID
    message = await channel.fetch_message(channel.last_message_id)
    return message
    
def create_conversation(starter): 
    query = '''INSERT INTO conversations (starter) VALUES (%s) RETURNING convo_id;'''
    cur.execute(query, [starter])
    db.commit()
    convo_id = cur.fetchall()[0][0]
    return convo_id

def get_search_card(searchID): 
    query = "SELECT resultID, filename FROM results WHERE searchID = %s;"
    cur.execute(query, [searchID])
    results = cur.fetchall()
    card = "```Results: \n"
    for num, name in results:
        card += str(num) + ". " + name + "\n"
    card += "```"
    return card

async def record_message(convoid):
    m = await get_latest_message()
    query = '''INSERT INTO messages (messageid, content, requestor, channelid, ts, convoid) VALUES (%s,%s,%s,%s,%s,%s);'''
    query_params = [m.id, m.content, m.author.id, m.channel.id, m.created_at.strftime("%Y-%m-%d %H:%M:%S"), convoid]
    cur.execute(query, query_params)
    db.commit()

def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r", newLine = "\n"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iterable    - Required  : iterable object (Iterable)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        newLine     - Optional  : new line
    """
    card_format = "```"
    total = 100
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        return_bar = f"{card_format}{prefix} {newLine} |{bar}| {percent}% {suffix} {card_format}"
        return return_bar
    return printProgressBar(iterable)

#------------------------------------------------------------------------------------------------------

#bot.run(open("/usr/src/app/secrets/bot-tokens/dev.txt").readline().strip())
bot.run(open("/home/cameron/projects/plex-bot/secrets/bot-tokens/dev.txt").readline().strip())