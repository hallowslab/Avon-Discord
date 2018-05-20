import datetime

avon_calls = ["Avon", "avon", "Hey avon", "hey avon", "Hey Avon"]
time_calls = ["WHAT TIME IS IT", "WHAT TIME IS IT?"]


async def Responses(message, client):
    ## Explicit messages
    if message.content == "AVON":
        await client.send_message(message.channel, "There is no need to yell...")
    for x in avon_calls:
        if message.content == x:
            await client.send_message(message.channel, "Yes? {}".format(message.author.mention))
    for x in time_calls:
        if message.content.upper() == x:
            time = str(datetime.datetime.now().time())
            await client.send_message(message.channel, "It's: " + time[:8] + " At: UTC")
