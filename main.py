import discord
import asyncio
from Avon import Adv_messages, messages, authenticated_commands, api_key, basic_commands

client = discord.Client()

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)

@client.event
async def on_message(message):
    await messages.Responses(message, client)
    await authenticated_commands.bot_commands(message, client)
    await authenticated_commands.music_commands(message, client)
    await authenticated_commands.page_speed_commands(message, client)
    await basic_commands.commands(message, client)
    await Adv_messages.Adv_responses(message, client)


client.run(api_key.token)
