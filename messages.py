import datetime


filter_these = ["FUCK","SHIT","CUNT"]

async def Responses(message, client):
    if message.content == "Avon" or message.content == "avon":
        await client.send_message(message.channel, "Yes? {}".format(message.author.mention))
    if message.content == "AVON":
        await client.send_message(message.channel, "There is no need to yell...")
    if message.content.upper() == "WHAT TIME IS IT?" or message.content.upper() == "WHAT TIME IS IT":
        time = str(datetime.datetime.now().time())
        await client.send_message(message.channel, "It's: " + time[:8] + " At: UTC")
