import sys
import logging
# This disables pylints warning about unused import since asyncio is being used
#pylint: disable=unused-import
import time
import discord
from discord.ext import commands
from Avon import messages, profanity_filter, config
from Avon.extensions import music_commands

bot = commands.Bot(command_prefix="!")
logger = logging.getLogger("Avon-Discord")


@bot.event
async def on_ready():
    """
    Triggers when the bot connects
    """
    logger.debug("Logged in as: %s ID: %s", bot.user.name, bot.user.id)


@bot.event
async def on_message(message):
    """
    Triggers when a message is sent to the server
    """
    await messages.responses(message, bot)
    # Not being used since it has a small API request limit
    # await profanity_filter.filter_messages(message, bot)
    await bot.process_commands(message)


def set_log_level(level):
    """
    Check if the log level is valid and if not sets it to default
    """
    n_level = getattr(logging, level.upper(), 20)
    if n_level == 20 and level.upper() != "INFO":
        sys.stdout.write("%s: %s\n" % ("Invalid log level", level))
    return n_level


def set_up_logger():
    """
    Function for setting up the logger and log level
    Also sets up the discord.py logger
    """
    # Avon-Discord log level from config
    l_level = config.settings["log_level"]
    n_level = set_log_level(l_level)

    # Avon logger
    formatter = logging.Formatter("%(name)s/%(funcName)s - %(levelname)s: %(message)s")
    logger.setLevel(n_level)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(n_level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    f_handler = logging.FileHandler(filename='Avon.log', encoding='utf-8', mode='w')
    #pylint: disable=line-too-long
    f_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s => %(funcName)20s: %(message)s'))
    logger.addHandler(f_handler)
    msg = "%s: %s" % ("Console logger is set with log level", l_level)
    logger.info(msg)

    # Discord logger
    dl_level = config.settings["discordpy_log_level"]
    if dl_level != "off":
        n_level = set_log_level(dl_level)
        d_logger = logging.getLogger('discord')
        d_logger.setLevel(n_level)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(n_level)
        stream_handler.setFormatter(formatter)
        d_logger.addHandler(stream_handler)
        f_handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
        f_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        logger.addHandler(f_handler)


if __name__ == "__main__":
    config.load_keys_and_settings()
    set_up_logger()
    start = time.perf_counter()
    bot.load_extension("Avon.authenticated_commands")
    end = time.perf_counter()
    logger.debug("Adding commands took %0.2f", (end - start))
    bot.run(config.access_keys["discord"])
