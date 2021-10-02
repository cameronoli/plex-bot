const { Client, Intents } = require('discord.js');
const dcord = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });
const cmd_prefix = '$';
//const qbit_api = require('qbittorrent-api');
//const qbt = qbit_api.connect('http://<container_name:port>');
const torrent_error = 'Please use a magent link or URL to torrent file. See "$help" for more information.';

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
        //qbt.add(args[1], <save_path>, args[0], function (error){messageCreate.channel.send(torrent_error)})
    }
    if(command === 'help' || command === 'h'){
        messageCreate.channel.send('this is the way')
    }
});

dcord.login('<enter bot token here>');