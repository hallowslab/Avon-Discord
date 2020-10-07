import logging
import asyncio
from discord.ext import commands
from Avon import config


logger = logging.getLogger("Avon-Discord")

async_state = type("", (), {})()
async_state.music_player = None
async_state.voice_channel = None


async def modify_state(state, var, val):
    """
    Modifies the variable in state with the provided value
    """
    logger.debug("Modifying state: %s => %s", state[var], val)
    state[var] = val
    await asyncio.sleep(0)
    return state


@commands.command()
@commands.has_any_role("DJ", "Admin")
async def playurl(ctx, url, state=async_state):
    """
    Plays the specified URL in MUSIC_CHANNEL
    """
    logger.debug("URL => %s", url)
    # FIXME: This is repeated multiple times across this commands,
    # TODO: Yeet this into another funtion
    if state.music_player is not None:
        logger.debug(state.music_player)
        await ctx.send("Music player is active use !queue to add a song to the queue")
        return
    channel_id = config.access_keys["music_channel_id"]
    logger.debug(type(channel_id))
    await ctx.send("Playing url %s in voice channel => %s" % (url, channel_id))
    # I still don't know if this works need to test it
    logger.debug("Music channel ID => %s", channel_id)
    channel = ctx.bot.get_channel(channel_id)
    logger.debug("Channel => %s", channel)
    voice_channel = await channel.connect()
    await modify_state(state, "voice_channel", voice_channel)
    player = await voice_channel.create_ytdl_player(url)
    await modify_state(state, "music_player", player)
    await ctx.send("Playing song provided in url on %s voice channel" % voice_channel)
    player.start()


@commands.command()
@commands.has_any_role("DJ", "Admin")
async def pause(ctx, arg, state=async_state):
    """
    Pauses the music player => can be resumed
    """
    logger.debug("Arg => %s", arg)
    if state.music_player is None:
        logger.debug(state.music_player)
        await ctx.send("Music player is not active")
        return
    await ctx.send("Pausing music")
    state.music_player.pause()


@commands.command()
@commands.has_any_role("DJ", "Admin")
async def stop(ctx, state=async_state):
    """
    Pauses the music player => cannot be resumed
    """
    if state.music_player is None:
        logger.debug(state.music_player)
        await ctx.send("Music player is not active")
        return
    await ctx.send("Stopping music player")
    state.music_player.stop()
    await modify_state(state, "music_player", None)
    voice_channel = ctx.bot.get_channel(config.access_keys["music_channel_id"])
    await ctx.send("Disconnecting")
    await voice_channel.disconnect()
    await voice_channel.cleanup()


@commands.command()
@commands.has_any_role("DJ", "Admin")
async def disconnect(ctx, state=async_state):
    """
    Disconnects the bot from the voice channel
    """
    if state.voice_channel is None:
        await ctx.send("Not connected to any voice channel")
        return
    await ctx.send("Disconnecting")
    await state.voice_channel.disconnect()
    await state.voice_channel.cleanup()
    await modify_state(state, "voice_channel", None)
    await modify_state(state, "music_player", None)


@commands.command()
@commands.has_any_role("DJ", "Admin")
async def resume(ctx, state=async_state):
    """
    Resumes the music player
    """
    if state.music_player is None:
        logger.debug(state.music_player)
        await ctx.send("Music player is active use !queue to add a song to the queue")
        return
    await ctx.send("Resuming music")
    state.music_player.resume()


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
