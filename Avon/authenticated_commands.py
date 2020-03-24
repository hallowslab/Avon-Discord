from Avon.api_key import master_id
#from Avon.api_key import speed_api
from Avon.Music.getFromPlaylist import read_playlist, show_all_langs, show_all_artists, find_by_artist, find_by_lang
import json
import youtube_dl
import time
import queue

Music_channel = "446734255561900056"
players = {}

######################## TODO: Must make bot be able to make calls and play songs by url ## REVIEW: Probably not possible


async def bot_commands(message ,client):
    if message.content.startswith("!"):
        if message.author.id == master_id:
            command = message.content[1:]
            if command.upper().startswith("CLOSE"):
                await client.logout()
        else:
            await message.channel.send("You do not have permissions to execute that")



async def page_speed_commands(message, client):
    if message.content.startswith("!"):
        if message.author.id == master_id:
            command = message.content[1:]
            if command.upper().startswith("TESTSPEED"):
                await message.channel.send("Testing speed")
        else:
            await message.channel.send("You do not have permissions to execute that")






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

async def music_commands(message , client):
    if message.content.startswith("!"):
        if message.author.id == master_id:
            command = message.content[1:]

            if command.upper().startswith("PLAYARTIST"):
                voice_channel = message.author.voice_channel
                server = message.server
                artist = command[11:]
                artist_songs = find_by_artist(artist)
                print(artist_songs)

                if voice_channel == None:
                    await message.channel.send("You don't seem to be connected to any voice channel")
                    return
                else:
                    print(artist)
                    print(artist_songs)
                    if "Error" in artist_songs.keys():
                        await message.channel.send(artist_songs)
                        return
                    else:
                        current_index = 0
                        all_urls = []
                        for song in artist_songs:
                            all_urls.append(artist_songs[song])
                        current_url = all_urls[current_index]

                        # Join voice channel create a player add it to
                        vc = await client.join_voice_channel(voice_channel)
                        player = await vc.create_ytdl_player(current_url)
                        players[server.id] = player
                        await message.channel.send("Playing song provided in url in {} voice channel".format(voice_channel))
                        player.start()

                        print("bananas")

                        start_time = time.time()
                        time.clock()
                        awaited = await wait_for_song(player, start_time)
                        if awaited == "Finished":
                            print("start new song")

            if command.upper().startswith("PLAYURL"):
                url = command[8:]
                voice_channel = message.author.voice_channel
                server = message.server

                if voice_channel == None:
                    await message.channel.send("You don't seem to be connected to any voice channel")
                    return
                else:
                    # Join voice channel create a player add it to
                    vc = await client.join_voice_channel(voice_channel)
                    player = await vc.create_ytdl_player(url)
                    players[server.id] = player
                    await message.channel.send("Playing song provided in url in {} voice channel".format(voice_channel))
                    player.start()



            if command.upper().startswith("PAUSE"):
                id = message.server.id
                players[id].pause()
                await message.channel.send("Pausing music")


            if command.upper().startswith("STOPMUSIC"):
                id = message.server.id
                players[id].stop()
                await message.channel.send("Stopping music")


            if command.upper().startswith("RESUME"):
                id = message.server.id
                players[id].resume()
                await message.channel.send("Resuming music")


            if command.upper().startswith("DISCONNECT"):
                server = message.server
                vc = client.voice_client_in(server)
                print("disconnecting")
                await vc.disconnect()


            if command.upper().startswith("SHOWPLAYLIST"):
                playlist = read_playlist()
                for item in playlist:
                    url = playlist[item]
                    await message.channel.send("```Found: {} at - {}```".format(item, url))
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
