from Avon.ping_host import ping
from Avon.Music.getFromPlaylist import show_all_langs, show_all_artists


async def commands(message, client):
    if message.content.startswith("!"):
        command = message.content[1:]
        if command[:4].upper() == "PING":
            if command[5:].upper() == "ROCKSTAR":
                host = "socialclub.rockstargames.com"
                if ping(host) == True:
                    await message.channel.send("Rockstar social club is online")
                else:
                    await message.channel.send("Rockstar social club seems to be down")
            host = command[5:]
            if ping(host) == True:
                await message.channel.send("Host is online")
            else:
                await message.channel.send("Host seems to be down, or refusing ping requests")
        if command.upper() == "SHOWLANGS":
            all_langs = show_all_langs()
            langs = ""
            for lang in all_langs:
                if lang != all_langs[-1]:
                    langs += lang + ", "
                else:
                    langs += lang
            await message.channel.send("```Languages are :{}```".format(langs))
        if command.upper() == "SHOWARTISTS":
            all_artists = show_all_artists()
            artists = ""
            for artist in all_artists:
                if artist != all_artists[-1]:
                    artists += artist + ", "
                else:
                    artists += artist
            await message.channel.send("```Artists are :{}```".format(artists))
