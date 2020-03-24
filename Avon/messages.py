import datetime

avon_calls = ["Avon", "avon", "Hey avon", "hey avon", "Hey Avon"]
time_calls = ["WHAT TIME IS IT", "WHAT TIME IS IT?"]


async def responses(message, client):
    if message.author == client.user:
        return
    ## Explicit messages
    if message.author == client.user:
        return
    if message.content == "AVON":
        await message.channel.send("There is no need to yell...")
    for x in avon_calls:
        if message.content == x:
            await message.channel.send("Yes? {}".format(message.author.mention))
    for x in time_calls:
        if message.content.upper() == x:
            time = str(datetime.datetime.now().time())
            await message.channel.send("It's: " + time[:8] + " at: UTC")
