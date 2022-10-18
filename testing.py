import qbittorrentapi

print("Logging in...")

qbt_client = qbittorrentapi.Client(host='192.168.1.20:8080', username='admin', password='adminadmin')
try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)

print("Logged in.")


def create_progress_card():
    global _ctx
    ctx = _ctx
    downloading_torrents = qbt_client.torrents_info("downloading")
    torrent_hashes = []
    if downloading_torrents == []:
        print("There are no torrents currently downloading.")
    else:
        for torrent in downloading_torrents:
            torrent_hash = torrent.get("hash")
            torrent_name = torrent.get("name")
            torrent_progress = round(torrent.get("progress") * 100, 2)
            progress_bar = progressBar(torrent_progress, torrent_name)
            await ctx.send(progress_bar)

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
    card_format = "'''"
    total = 100
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        return_bar = f"{card_format}{prefix} {newLine} |{bar}| {percent}% {suffix} {card_format}"
        print(return_bar)
    printProgressBar(iterable)

    
create_progress_card()