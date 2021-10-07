const { Client, Intents } = require('discord.js');
const dcord = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });
const cmd_prefix = '$';

const qbittorrentapi = require('qbittorrent-api-v2');
const qbt_client = qbittorrentapi.Client(host='torrent:8080', username='admin', password='adminadmin');
//const qbt_api = require('qbittorrent-api-v2');
//const qbt = qbt_api.connect('test_torrent:8080', 'admin', 'adminadmin');
console.log(qbt_client.app.version);

const torrent_error = 'Please use a magent link or a URL to a torrent file. See "$help" for more information.';
const help_file = 'This is a bot for adding movies or T.V shows to the Plex media server "Beauty" \n \
Bot Commands \n \
- $ping; Returns "Pong!" \n \
- $dl, $download {type} {link} \n \
    - {type}; Use "movie" when downloading a movie or "tv" when downloading a T.V show \n \
    - {link}; You must use either a magnet link or a Url to a torrent file \n \
        E.G. - Magnet: magnet:?xt=urn:btih:f5caf1161cbe9312511cf1c35a75c744e7eb8e67&dn=Survivor.S41E02.1080p%5D \n \
             - Url: https://rarbg.to/download.php?id=mhy6u3a&h=f5c&f=Survivor.S41E02.1080p.AMZN.WEBRip.DDP5.1.x264-KiNGS%5Brartv%5D-[rarbg.to].torrent \n \
             '
dcord.once('ready', () =>{
    console.log('PlexBot is online!');
});

dcord.on('message', messageCreate =>{
    if(!messageCreate.content.startsWith(cmd_prefix) || messageCreate.author.bot) return;

    const args = messageCreate.content.slice(cmd_prefix.length).split(/ +/);
    const command = args.shift().toLowerCase();

    if(command === 'ping'){
        messageCreate.channel.send('pong!');
    }
    if(command === 'download' || command === 'dl'){
        messageCreate.channel.send('Downloading ' + String(args[0]) + ' with ' + String(args[1]));
        qbt.add(args[1], "/downloads", args[0], function (error){messageCreate.channel.send(torrent_error)});
    }
    if(command === 'help' || command === 'h'){
        messageCreate.channel.send(help_file)
    }
});

dcord.login('token');