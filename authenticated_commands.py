from api_key import master_id
from api_key import page_speed

async def Commands(message, client):
    if message.content.startswith("!"):
        if message.author.id == master_id:
            command = message.content[1:]
            if command.upper().startswith("TESTSPEED"):
                await client.send_message(message.channel, "Testing speed")
            if command.upper().startswith("CLOSE"):
                await client.logout()
        else:
            await client.send_message(message.channel , "You do not have permissions to execute that")
