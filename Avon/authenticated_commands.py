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
            await client.send_message(message.channel , "You do not have permissions to execute that")



async def page_speed_commands(message, client):
    if message.content.startswith("!"):
        if message.author.id == master_id:
            command = message.content[1:]
            if command.upper().startswith("TESTSPEED"):
                await client.send_message(message.channel, "Testing speed")
        else:
            await client.send_message(message.channel , "You do not have permissions to execute that")






# # TODO: Create function for queueing songs # FIXME: Update after=lambda: **
# if command.upper().startswith("PLAY"):
#     Playlist = command[5:]
#     voice_channel = message.author.voice_channel
#     server = message.server
#     if voice_channel == None:
#         await client.send_message(message.channel, "You don't seem to be connected to any voice channel")
#         return
#     await client.send_message(message.channel, "Playing song provided in url in {} voice channel".format(voice_channel))
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
                    await client.send_message(message.channel, "You don't seem to be connected to any voice channel")
                    return
                else:
                    print(artist)
                    print(artist_songs)
                    if "Error" in artist_songs.keys():
                        await client.send_message(message.channel, artist_songs)
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
                        await client.send_message(message.channel, "Playing song provided in url in {} voice channel".format(voice_channel))
                        player.start()

                        start_time = time.time()
                        time.clock()
                        awaited = await wait_for_song(player, start_time)
                        if awaited == "Finished":
                            print("start new song")

            if command.upper().startswith("TESTLAMBDA"):
                artist = command[11:]
                artist_songs = find_by_artist(artist)
                current_index = 0
                all_urls = []
                for song in artist_songs:
                    all_urls.append(artist_songs[song])
                url = None
                if url is None:
                    #function is being called from after (this will be explained in the next function)
                    if all_urls.size() > 0:
                        #fetch from queue
                        url = all_urls.dequeue()
                    else:
                        #Unset stored objects, also possibly disconnect from voice channel here
                        player = None
                        voice = None
                        return
                if player is None:
                    #no one is using the stream player, we can start playback immediately
                    player = await self.voice.create_ytdl_player(url, after=lambda: play_next(client, message))
                    player.start()
                else:
                    if player.is_playing():
                        #called by the user to add a song
                        all_urls.enqueue(url)
                    else:
                        #this section happens when a song has finished, we play the next song here
                        player = await self.voice.create_ytdl_player(url, after=lambda: play_next(client, message))
                        player.start()

            if command.upper().startswith("PLAYURL"):
                url = command[8:]
                voice_channel = message.author.voice_channel
                server = message.server

                if voice_channel == None:
                    await client.send_message(message.channel, "You don't seem to be connected to any voice channel")
                    return
                else:
                    # Join voice channel create a player add it to
                    vc = await client.join_voice_channel(voice_channel)
                    player = await vc.create_ytdl_player(url)
                    players[server.id] = player
                    await client.send_message(message.channel, "Playing song provided in url in {} voice channel".format(voice_channel))
                    player.start()



            if command.upper().startswith("PAUSE"):
                id = message.server.id
                players[id].pause()
                await client.send_message(message.channel, "Pausing music")


            if command.upper().startswith("STOPMUSIC"):
                id = message.server.id
                players[id].stop()
                await client.send_message(message.channel, "Stopping music")


            if command.upper().startswith("RESUME"):
                id = message.server.id
                players[id].resume()
                await client.send_message(message.channel, "Resuming music")


            if command.upper().startswith("DISCONNECT"):
                server = message.server
                vc = client.voice_client_in(server)
                print("disconnecting")
                await vc.disconnect()


            if command.upper().startswith("SHOWPLAYLIST"):
                playlist = read_playlist()
                for item in playlist:
                    url = playlist[item]
                    await client.send_message(message.channel, "```Found: {} at - {}```".format(item, url))
        else:
            await client.send_message(message.channel , "You do not have permissions to execute that")


def play_next(client, message):
    asyncio.run_coroutine_threadsafe(play_music(client, message), client.loop)



async def wait_for_song(player, st_time):
    elapsed = 0
    wait_timer = 0
    running = True
    if elapsed < player.duration + 3:
        elapsed = time.time() - st_time
        wait_timer = time.time() - st_time
        if wait_timer >= 20:
            wait_timer = 0
    if elapsed >= player.duration + 3:
        print("Song finished")
        running = False
        return("Finished")
