import discord, asyncio
from discord.ext import commands
from discord.ext.commands import Bot
from api_key import token
from api_key import master_id

Client = discord.Client()
bot = Bot(command_prefix = "!")

@bot.event
async def on_ready():
    print("Ready")

@bot.event
async def on_message(message):
    # Messages
    if message.content.upper() == "COOKIE":
        await bot.send_message(message.channel, ":cookie:")
    if message.content == "Avon":
        await bot.send_message(message.channel, "Yes?")
    if message.content == "avon":
        await bot.send_message(message.channel, "Yes?")
    if message.content == "AVON":
        await bot.send_message(message.channel, "There is no need to yell you cunt")
        # Commands
    if message.content.startswith("!Close"):
        # Command that requires auth
        if message.author.id == master_id:
            await bot.close()
        else:
            await bot.send_message(message.channel, "Fuck Off!")

@bot.command(pass_context = True)
async def Close(ctx):
    await bot.close()


bot.run(token)
