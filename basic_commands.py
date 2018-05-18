async def commands(message, client):
    if message.content.startswith("!"):
        if message.author.id == master_id:
            command = message.content[1:]
            print(command)
            if command.upper() == "CLOSE":
                await client.logout()
        else:
            await client.send_message(message.channel , "Fuck off!")
