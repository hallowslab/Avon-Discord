import logging
import time
from discord.ext import commands
from Avon import config


logger = logging.getLogger("Avon-Discord")


MUSIC_PLAYER = None
# Don't know if this helps at all but it is supposed to prevent
# music_commands from overwritting a global variable while it is in use
IS_PLAYER_BUSY = False

@commands.command()
async def playurl(ctx, url: str):
    """
    Plays the specified URL in MUSIC_CHANNEL
    """
    await ctx.send("Playing url %s in voice channel => %s" % (url))


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
            logger.debug("Locking global variable MUSIC_PLAYER")
            IS_PLAYER_BUSY = True
            # Broken due to new updates
            if command.upper().startswith("PLAYURL"):
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

def setup(bot):
    """
    Function to load commands as a bot extension
    """
    cmds = [
    ]
    for command in cmds:
        bot.add_command(command)
