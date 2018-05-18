import discord, asyncio
from discord.ext import commands
from discord.ext.commands import Bot
from api_key import token

Client = discord.Client()
bot = Bot(command_prefix = "!")

@bot.event
async def on_ready():
    print("Ready")

@bot.event
async def on_message(message):
    if message.content.upper() == "COOKIE":
        await bot.send_message(message.channel, ":cookie:")
    if message.content == "Avon":
        await bot.send_message(message.channel, "Yes?")
    if message.content == "avon":
        await bot.send_message(message.channel, "Yes?")
    if message.content == "AVON":
        await bot.send_message(message.channel, "There is no need to yell you cunt")
    if message.content.startswith("!Close"):
        await bot.close()

@bot.command(pass_context = True)
async def Close(ctx):
    await bot.close()


bot.run(token)
