import datetime

async def Responses(message, client):
    if message.content == "Avon":
        await client.send_message(message.channel, "Yes?")
    if message.content == "avon":
        await client.send_message(message.channel, "Yes?")
    if message.content == "AVON":
        await client.send_message(message.channel, "There is no need to yell you cunt")
    if message.content.upper() == "WHAT TIME IS IT?":
        time = str(datetime.datetime.now().time())
        await client.send_message(message.channel, "It's: " + time[:8] + " At: UTC")
