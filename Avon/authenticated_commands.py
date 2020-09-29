import logging
import time
#pylint: disable=unused-import
import youtube_dl
from Avon import config
from Avon.ping_host import ping

MUSIC_PLAYER = None

logger = logging.getLogger("Avon-Discord")

async def admin_commands(message ,client):
    """
    Server administrator commands
    """
    if message.author == client.user:
        return
    if message.content.startswith("!"):
        if str(message.author.id) == config.access_keys["master_id"]:
            command = message.content[1:]

            if command.upper().startswith("CLOSE"):
                await message.channel.send("Logging out!")
                await client.logout()

            # Unfinished
            if command.upper().startswith("TESTSPEED"):
                await message.channel.send("Testing speed")
                await message.channel.send("Not implemented")
    else:
        await message.channel.send("You do not have permissions to execute that")


async def music_commands(message, client):
    """
    Commands for playing, pausing, stopping music
    """
    #pylint: disable=global-statement
    global MUSIC_PLAYER
    if message.author == client.user:
        return
    if message.content.startswith("!"):
        if str(message.author.id) == config.access_keys["master_id"]:
            command = message.content[1:]
            # Broken due to new updates
            if command.upper().startswith("PLAYURL"):
                url = command[8:]
                # Join voice channel create a player add it to
                # TODO: Add a way to pass voice channel trough message
                channel =  client.get_channel(config.access_keys["Music_channel_id"])
                voice_channel = await channel.connect()
                player = await voice_channel.create_ytdl_player(url)
                MUSIC_PLAYER = player
                await message.channel.send("Playing song provided in \
                                           url on %s voice channel" % voice_channel)
                player.start()


            # Pauses music - can be resumed
            if command.upper().startswith("PAUSE"):
                MUSIC_PLAYER.pause()
                await message.channel.send("Pausing music")

            # Stops music - cannot be resumed
            if command.upper().startswith("STOPMUSIC"):
                MUSIC_PLAYER.stop()
                MUSIC_PLAYER = None
                await message.channel.send("Stopping music")

            # Resumes music
            if command.upper().startswith("RESUME"):
                MUSIC_PLAYER.resume()
                await message.channel.send("Resuming music")

            # Disconnects from the voice channel
            if command.upper().startswith("DISCONNECT"):
                MUSIC_PLAYER.stop()
                MUSIC_PLAYER = None
                voice_channel = client.get_channel(config.access_keys["Music_channel_id"])
                logger.info("disconnecting")
                await voice_channel.disconnect()
        else:
            await message.channel.send("You do not have permissions to execute that")


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
                if command[5:].upper() == "ROCKSTAR":
                    host = "socialclub.rockstargames.com"
                    if ping(host):
                        await message.channel.send("Rockstar social club is online")
                    else:
                        await message.channel.send("Rockstar social club seems to be down")
                    host = command[5:]
                    if ping(host):
                        await message.channel.send("Host is online")
                    else:
                        await message.channel.send("Host seems to be down, \
                                                   or refusing ping requests")
        else:
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


# # TODO: Create function for queueing songs # FIXME: Update after=lambda: **
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
    #player = await vc.create_ytdl_player(url, after=lambda: ## TODO: Function to run)
    #players[server.id] = player
    #player.start()
