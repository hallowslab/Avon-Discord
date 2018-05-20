import discord
import asyncio
from api_key import token
from authenticated_commands import Commands
from messages import Responses
from basic_commands import commands
from Adv_messages import Adv_responses

client = discord.Client()

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)

@client.event
async def on_message(message):
    await Responses(message, client)
    await Commands(message, client)
    await commands(message, client)
    await Adv_responses(message, client)


client.run(token)
