from Avon.ping_host import ping
from Avon.Music.getFromPlaylist import show_all_langs, show_all_artists


async def commands(message, client):
    if message.content.startswith("!"):
        command = message.content[1:]
        if command[:4].upper() == "PING":
            if command[5:].upper() == "ROCKSTAR":
                host = "socialclub.rockstargames.com"
                if ping(host) == True:
                    await client.send_message(message.channel, "Rockstar social club is online")
                else:
                    await client.send_message(message.channel, "Rockstar social club seems to be down")
            host = command[5:]
            if ping(host) == True:
                await client.send_message(message.channel, "Host is online")
            else:
                await client.send_message(message.channel, "Host seems to be down, or refusing ping requests")
        if command.upper() == "SHOWLANGS":
            all_langs = show_all_langs()
            langs = ""
            for lang in all_langs:
                if lang != all_langs[-1]:
                    langs += lang + ", "
                else:
                    langs += lang
            await client.send_message(message.channel, "```Languages are :{}```".format(langs))
        if command.upper() == "SHOWARTISTS":
            all_artists = show_all_artists()
            artists = ""
            for artist in all_artists:
                if artist != all_artists[-1]:
                    artists += artist + ", "
                else:
                    artists += artist
            await client.send_message(message.channel, "```Artists are :{}```".format(artists))
