import logging
import time
import asyncio
from discord.ext import commands
from Avon import config


logger = logging.getLogger("Avon-Discord")


async_state = type("", (), {})()
async_state.music_player = None
async_state.is_player_busy = False


async def modify_state(state, var, val):
    """
    Modifies the variable in state with the provided value
    """
    state[var] = val
    await asyncio.sleep(0)
    return state


@commands.command()
async def playurl(ctx, url: str, state=async_state):
    """
    Plays the specified URL in MUSIC_CHANNEL
    """
    if str(ctx.message.author.id) == config.access_keys["master_id"]:
        await modify_state(state, "is_player_busy", True)
        # FIXME: This is repeated multiple times across this commands,
        # TODO: Yeet this into another funtion
        if state.is_player_busy:
            logger.debug("Music player is busy")
            await ctx.send("Music player is currently busy")
            await modify_state(state, "is_player_busy", False)
            return
        if state.music_player is not None:
            logger.debug(state.music_player)
            await ctx.send("Music player is active use !queue to add a song to the queue")
            await modify_state(state, "is_player_busy", False)
            return
        await ctx.send("Playing url %s in voice channel => %s" % (url))
        channel_id = config.access_keys["music_channel_id"]
        logger.debug("Music channel ID => %s", channel_id)
        channel = ctx.bot.get_channel(channel_id)
        logger.debug("Channel => %s" % channel)
        voice_channel = await channel.connect()
        player = await voice_channel.create_ytdl_player(url)
        await modify_state(state, "music_player", player)
        await ctx.send("Playing song provided in url on %s voice channel" % voice_channel)
        player.start()
        await modify_state(state, "is_player_busy", False)
    else:
        await ctx.send("You don't have permissions to execute that")


@commands.command()
async def pause(ctx, state=async_state):
    if str(ctx.message.author.id) == config.access_keys["master_id"]:
        await modify_state(state, "is_player_busy", True)
        if state.is_player_busy:
            logger.debug("Music player is busy")
            await ctx.send("Music player is currently busy")
            await modify_state(state, "is_player_busy", False)
            return
        if state.music_player is None:
            logger.debug(state.music_player)
            await ctx.send("Music player is not active")
            await modify_state(state, "is_player_busy", False)
            return
        await ctx.send("Pausing music")
        state.music_player.pause()
    else:
        await ctx.send("You don't have permissions to execute that")


@commands.command()
async def stop(ctx, state=async_state):
    if str(ctx.message.author.id) == config.access_keys["master_id"]:
        await modify_state(state, "is_player_busy", True)
        if state.is_player_busy:
            logger.debug("Music player is busy")
            await ctx.send("Music player is currently busy")
            await modify_state(state, "is_player_busy", False)
            return
        if state.music_player is None:
            logger.debug(state.music_player)
            await ctx.send("Music player is not active")
            await modify_state(state, "is_player_busy", False)
            return
        await ctx.send("Stopping music player")
        state.music_player.stop()
        state.music_player = None
        voice_channel = ctx.bot.get_channel(config.access_keys["music_channel_id"])
        await ctx.send("Disconnecting")
        await voice_channel.disconnect()
        await voice_channel.cleanup()
    else:
        await ctx.send("You don't have permissions to execute that")


@commands.command()
async def resume(ctx, state=async_state):
    if str(ctx.message.author.id) == config.access_keys["master_id"]:
        await modify_state(state, "is_player_busy", True)
        if state.is_player_busy:
            logger.debug("Music player is busy")
            await ctx.send("Music player is currently busy")
            await modify_state(state, "is_player_busy", False)
            return
        if state.music_player is None:
            logger.debug(state.music_player)
            await ctx.send("Music player is active use !queue to add a song to the queue")
            await modify_state(state, "is_player_busy", False)
            return
        await ctx.send("Resuming music")
        state.music_player.resume()
    else:
        await ctx.send("You don't have permissions to execute that")


def setup(bot):
    """
    Function to load commands as a bot extension
    """
    cmds = [
        playurl,
        pause,
        stop,
        resume
    ]
    for command in cmds:
        bot.add_command(command)
