import logging
import datetime

logger = logging.getLogger("Avon-Discord")

time_calls = ["WHAT TIME IS IT", "WHAT IS THE TIME", "WHAT TIME IT IS"]

async def responses(message, client):
    """
    Regular messages and responses
    """
    if message.author == client.user:
        return
    if message.content.upper.startswith() == "AVON":
        await message.channel.send("There is no need to yell...")
    if message.content.upper() in time_calls:
        time = str(datetime.datetime.now().time())
        await message.channel.send("It's: " + time[:8] + " at: UTC")
