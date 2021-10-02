const { Client, Intents } = require('discord.js');
const dcord = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });
const cmd_prefix = '$';
//const qbit_api = require('qbittorrent-api');
//const qbt = qbit_api.connect('<can't use contnainer name in swarm>:14715');
const torrent_error = 'Please use a magent link or a URL to a torrent file. See "$help" for more information.';
const help_file = 'This is a bot for adding movies or T.V shows to the Plex media server "Beauty"\
Bot Commands\
- $ping; Returns "Pong!"\
- $dl, $download {type} {link}\
    - {type}; Use "movie" when downloading a movie or "tv" when downloading a T.V show\
    - {link}; You must use either a magnet link or a URL to a torrent file\
        E.G. - Magnet: magnet:?xt=urn:btih:f5caf1161cbe9312511cf1c35a75c744e7eb8e67&dn=Survivor.S41E02.1080p.AMZN.WEBRip.DDP5.1.x264-KiNGS%5Brartv%5D&tr=http%3A%2F%2Ftracker.trackerfix.com%3A80%2Fannounce&tr=udp%3A%2F%2F9.rarbg.me%3A2950&tr=udp%3A%2F%2F9.rarbg.to%3A2940&tr=udp%3A%2F%2Ftracker.fatkhoala.org%3A13750&tr=udp%3A%2F%2Ftracker.slowcheetah.org%3A14800\
             - URL: https://rarbg.to/download.php?id=mhy6u3a&h=f5c&f=Survivor.S41E02.1080p.AMZN.WEBRip.DDP5.1.x264-KiNGS%5Brartv%5D-[rarbg.to].torrent\
             ';

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
        //qbt.add(args[1], <save_path (volume - media?)>, args[0], function (error){messageCreate.channel.send(torrent_error)})
    }
    if(command === 'help' || command === 'h'){
        messageCreate.channel.send(help_file)
    }
});

dcord.login('<enter bot token here>');