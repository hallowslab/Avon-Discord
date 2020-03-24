from Avon.api_key import master_id
#from Avon.api_key import speed_api
import json
import youtube_dl
import time
import queue

music_player = None

async def admin_commands(message ,client):
    if message.author == client.user:
        return
    if message.content.startswith("!"):
        if str(message.author.id) == master_id:
            command = message.content[1:]

            if command.upper().startswith("CLOSE"):
                await message.channel.send("Logging out!")
                await client.logout()

            # Unfinished
            if command.upper().startswith("TESTSPEED"):
                await message.channel.send("Testing speed")

            # Broken due to new updates
            if command.upper().startswith("PLAYURL"):
                url = command[8:]
                # Join voice channel create a player add it to
                channel =  client.get_channel(692018702710865921)
                vc = await channel.connect()
                player = await vc.create_ytdl_player(url)
                music_player = player
                await message.channel.send("Playing song provided in url in {} voice channel".format(voice_channel))
                player.start()



            if command.upper().startswith("PAUSE"):
                music_player.pause()
                await message.channel.send("Pausing music")

            if command.upper().startswith("STOPMUSIC"):
                music_player.stop()
                await message.channel.send("Stopping music")

            if command.upper().startswith("RESUME"):
                music_player.resume()
                await message.channel.send("Resuming music")

            if command.upper().startswith("DISCONNECT"):
                server = message.server
                vc = client.voice_client_in(server)
                print("disconnecting")
                await vc.disconnect()
        else:
            await message.channel.send("You do not have permissions to execute that")


async def wait_for_song(player, st_time):
    elapsed = 0
    wait_timer = 20
    running = True
    while True:
        if elapsed < player.duration:
            elapsed = time.time() - st_time
        if elapsed >= player.duration:
            print("Song finished")
            running = False
            print("Finished")
            return("Finished")


# # TODO: Create function for queueing songs # FIXME: Update after=lambda: **
# if command.upper().startswith("PLAY"):
#     Playlist = command[5:]
#     voice_channel = message.author.voice_channel
#     server = message.server
#     if voice_channel == None:
#         await message.channel.send("You don't seem to be connected to any voice channel")
#         return
#     await message.channel.send("Playing song provided in url in {} voice channel".format(voice_channel))
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