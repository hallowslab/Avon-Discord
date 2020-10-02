import logging
import time
#pylint: disable=unused-import
import youtube_dl
import discord
from discord.ext import commands
from Avon import config
from Avon.ping_host import ping

MUSIC_PLAYER = None
# Don't know if this helps at all but it is supposed to prevent
# music_commands from overwritting a global variable while it is in use
IS_PLAYER_BUSY = False

logger = logging.getLogger("Avon-Discord")


@commands.command()
async def close(ctx):
    """
    Closes the bot connection
    """
    if str(ctx.message.author.id) == config.access_keys["master_id"]:
        await ctx.send("Logging out!")
        await ctx.bot.logout()
    else:
        await ctx.send("You do not have permissions to execute that!")

@commands.command()
async def kick(ctx, member: discord.Member, reason: str = None):
    """
    kicks the member and specifies reason
    """
    if str(ctx.message.author.id) == config.access_keys["master_id"]:
        reason = "No reason defined" if reason is None else reason
        await ctx.send("Kicking user %s, reason: %s" % (member, reason))
        await member.kick(reason=reason)
    else:
        await ctx.send("You do not have permissions to execute that!")

@commands.command()
async def ban(ctx, member: discord.Member, reason: str = None):
    """
    kicks the member and specifies reason
    """
    if str(ctx.message.author.id) == config.access_keys["master_id"]:
        reason = "No reason defined" if reason is None else reason
        await ctx.send("Kicking user %s, reason: %s" % (member, reason))
        await member.kick(reason=reason)
    else:
        await ctx.send("You do not have permissions to execute that!")


async def admin_commands(message ,client):
    """
    Server administrator commands
    """
    if message.author == client.user:
        return
    if str(message.author.id) == config.access_keys["master_id"]:
        if message.content.startswith("!"):
            command = message.content[1:]
            # TODO: Unfinished
            if command.upper().startswith("TESTSPEED"):
                # await message.channel.send("Testing speed")
                await message.channel.send("Not implemented")
    else:
        logger.debug("Insufficient permissions")
        await message.channel.send("You do not have permissions to execute that")


async def music_commands(message, client):
    """
    Commands for playing, pausing, stopping music
    """
    #pylint: disable=global-statement
    global MUSIC_PLAYER
    global IS_PLAYER_BUSY
    if message.author == client.user:
        return
    if IS_PLAYER_BUSY:
        logger.debug("Music player is busy")
        await message.channel.send("Music player is currently busy")
        return
    if message.content.startswith("!"):
        if str(message.author.id) == config.access_keys["master_id"]:
            command = message.content[1:]
            logger.debug("Command => %s", command)
            # Broken due to new updates
            if command.upper().startswith("PLAYURL"):
                IS_PLAYER_BUSY = True
                if MUSIC_PLAYER is not None:
                    logger.debug("MUSIC_PLAYER obj => %s", MUSIC_PLAYER)
                    await message.channel.send("Music player is already active")
                    IS_PLAYER_BUSY = False
                    return
                url = command[8:]
                logger.debug("url => %s", url)
                # Join voice channel create a player add it to MUSIC_PLAYER variable
                channel_id = config.access_keys["music_channel_id"]
                logger.debug("Music channel ID: %s", channel_id)
                channel = client.get_channel(channel_id)
                logger.debug(channel)
                voice_channel = await channel.connect()
                player = await voice_channel.create_ytdl_player(url)
                MUSIC_PLAYER = player
                await message.channel.send("Playing song provided in \
                                           url on %s voice channel" % voice_channel)
                player.start()

            # Disconnects from the voice channel
            # TODO: This should disconnect when the music finishes
            # since stop music already disconnects and cleans up the player
            # if command.upper().startswith("DISCONNECT"):
            #     MUSIC_PLAYER.stop()
            #     MUSIC_PLAYER = None
            #     voice_channel = client.get_channel(config.access_keys["music_channel_id"])
            #     await message.channel.send("Disconnecting")
            #     await voice_channel.disconnect()
            #     await voice_channel.cleanup()

            # FIXME: This needs to be more specific since it triggers for any command
            if MUSIC_PLAYER is None:
                await message.channel.send("Music player is not active")
                IS_PLAYER_BUSY = False
                return

            # Pauses music - can be resumed
            if command.upper().startswith("PAUSE"):
                MUSIC_PLAYER.pause()
                await message.channel.send("Pausing music")

            # Stops music - cannot be resumed
            if command.upper().startswith("STOPMUSIC"):
                MUSIC_PLAYER.stop()
                MUSIC_PLAYER = None
                await message.channel.send("Stopping music")
                voice_channel = client.get_channel(config.access_keys["music_channel_id"])
                await message.channel.send("Disconnecting")
                await voice_channel.disconnect()
                await voice_channel.cleanup()

            # Resumes music
            if command.upper().startswith("RESUME"):
                MUSIC_PLAYER.resume()
                await message.channel.send("Resuming music")
        else:
            logger.debug("Insufficient permissions")
            await message.channel.send("You do not have permissions to execute that")
    IS_PLAYER_BUSY = False


async def system_commands(message, client):
    """
    Commands that call system functionality
    """
    if message.author == client.user:
        return
    if message.content.startswith("!"):
        if str(message.author.id) == config.access_keys["master_id"]:
            command = message.content[1:]
            if command[:4].upper() == "PING":
                host = command[5:]
                if ping(host):
                    await message.channel.send("Host is online")
                else:
                    await message.channel.send("Host seems to be down, \
                                                or refusing ping requests")
        else:
            logger.debug("Insufficient permissions")
            await message.channel.send("You do not have permissions to execute that")


async def wait_for_song(player, st_time):
    """
    I dont remember why i wrote this
    """
    elapsed = 0
    #pylint: disable=unused-variable
    wait_timer = 20
    #pylint: disable=unused-variable
    running = True
    while True:
        if elapsed < player.duration:
            elapsed = time.time() - st_time
            if elapsed >= player.duration:
                print("Song finished")
                running = False
                print("Finished")
                return "Finished"


# # TODO: Create function for queueing songs
# if command.upper().startswith("PLAY"):
#     Playlist = command[5:]
#     voice_channel = message.author.voice_channel
#     server = message.server
#     if voice_channel == None:
#         await message.channel.send("You don't seem to be connected to any voice channel")
#         return
#     await message.channel.send("Playing song provided in \
#                                url in {} voice channel".format(voice_channel))
#     vc = await client.join_voice_channel(voice_channel)
#     #player = await vc.create_ytdl_player(url)
#     start = time.time()
#     time.clock()
#     elapsed = 0
    #while elapsed < player.duration:
    #    elapsed = time.time() - start
    #    print("Song playing")
    #if elapsed > player.duration:
    #    print("Song Finished")
    #    return
    #
    #player = await vc.create_ytdl_player(url, after=lambda: ## FIXME: Function to run)
    #players[server.id] = player
    #player.start()
