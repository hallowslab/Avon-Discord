async def Responses(message, client):
    if message.content == "Avon":
        await client.send_message(message.channel, "Yes?")
    if message.content == "avon":
        await client.send_message(message.channel, "Yes?")
    if message.content == "AVON":
        await client.send_message(message.channel, "There is no need to yell you cunt")
