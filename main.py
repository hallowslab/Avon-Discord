import sys
import logging
# This disables pylints warning about unused import since asyncio is being used
#pylint: disable=unused-import
import asyncio
import discord
from Avon import messages, authenticated_commands, profanity_filter, config

client = discord.Client()
logger = logging.getLogger("Avon-Discord")

@client.event
async def on_ready():
    """
    Triggers when the client connects
    """
    logger.debug("Logged in as: %s ID: %s", client.user.name, client.user.id)


@client.event
async def on_message(message):
    """
    Triggers when a message is sent to the server
    """
    await messages.responses(message, client)
    await profanity_filter.filter_messages(message, client)
    await authenticated_commands.admin_commands(message, client)
    await authenticated_commands.music_commands(message, client)
    await authenticated_commands.system_commands(message, client)


def set_up_logger():
    """
    Function for setting up the logger and log level
    Also sets up the discord.py logger
    """
    l_level = config.settings["log_level"]
    n_level = getattr(logging, l_level.upper(), 20)
    if n_level == 20 and l_level.upper() != "INFO":
        sys.stdout.write("%s: %s\n" % ("Invalid log level", l_level))

    # Avon logger
    formatter = logging.Formatter("%(name)s/%(funcName)s - %(levelname)s: %(message)s")
    logger.setLevel(n_level)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(n_level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    f_handler = logging.FileHandler(filename='Avon.log', encoding='utf-8', mode='w')
    f_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s => %(funcName)20s: %(message)s'))
    logger.addHandler(f_handler)
    msg = "%s: %s" % ("Console logger is set with log level", l_level)
    logger.info(msg)

    # Discord logger
    dl_level = config.settings["discordpy_log_level"]
    d_logger = logging.getLogger('discord')
    d_logger.setLevel(dl_level)
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
    client.run(config.access_keys["Discord"])
