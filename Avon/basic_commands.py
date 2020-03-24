from Avon.ping_host import ping

async def commands(message, client):
    if message.author == client.user:
        return
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
