from Avon.ping_host import ping
from Avon.Music.getFromPlaylist import showAllGenres, showAllArtists


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
        if command.upper() == "SHOWGENRES":
            genres = showAllGenres()
            await client.send_message(message.channel, "```Genres are :{}```".format(genres))
        if command.upper() == "SHOWARTISTS":
            artists = showAllArtists()
            await client.send_message(message.channel, "```Artists are :{}```".format(artists))
