
its_Avon = ["aVon", "avOn", "avoN", "AVoN", "AvON", "AvoN", "aVON", "av0n", "Av0n", "AV0N", "AVOn"]
filter_these = ["FUCK","SHIT","CUNT", "BITCH","MOTHERFUCKER","COCK","COCKSUCKER", "DICK", "PUSSY", "WHORE"]

async def Adv_responses(message, client):
    separated_messages = message.content.split()
    for x in separated_messages:
        for y in its_Avon:
            if x == y:
                await client.send_message(message.channel, "It's Avon ....")
        for y in filter_these:
            if x.upper() == y:
                await client.delete_message(message)
                await client.send_message(message.channel, "Watch yo profanity")
        if x.upper() == "DRUGS":
            await client.delete_message(message)
            await client.send_message(message.channel, "I'm watching you {} :police_car:".format(message.author.mention))
