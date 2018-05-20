import discord
import asyncio
from api_key import token
from basic_commands import commands
from Avon import Adv_messages, messages, authenticated_commands

client = discord.Client()

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)

@client.event
async def on_message(message):
    await messages.Responses(message, client)
    await authenticated_commands.Commands(message, client)
    await commands(message, client)
    await Adv_messages.Adv_responses(message, client)


client.run(token)
