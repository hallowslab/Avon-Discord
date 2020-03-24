import discord
import asyncio
from Avon.api_key import token
from Avon import messages, authenticated_commands, api_key, basic_commands, profanity_filter

client = discord.Client()

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)

@client.event
async def on_message(message):
    await messages.responses(message, client)
    await profanity_filter.filter_messages(message, client)
    await authenticated_commands.bot_commands(message, client)
    await authenticated_commands.music_commands(message, client)
    await authenticated_commands.page_speed_commands(message, client)
    await basic_commands.commands(message, client)


client.run(token)
