from Avon.api_key import master_id
from Avon.api_key import speed_api
from Avon.Music.getFromPlaylist import readPlaylist
import json
import youtube_dl

Music_channel = "446734255561900056"
players = {}

######################## TODO: Must make bot be able to make calls and play songs by url ## REVIEW: Probably not possible



async def Commands(message, client):
    if message.content.startswith("!"):
        if message.author.id == master_id:
            command = message.content[1:]
            if command.upper().startswith("TESTSPEED"):
                await client.send_message(message.channel, "Testing speed")
            # # TODO: Create function for queueing songs # FIXME: Update after=lambda: **
            if command.upper().startswith("PLAY"):
                Playlist = command[5:]
                voice_channel = message.author.voice_channel
                server = message.server
                if voice_channel == None:
                    await client.send_message(message.channel, "You don't seem to be connected to any voice channel")
                    return
                await client.send_message(message.channel, "Playing song provided in url in {} voice channel".format(voice_channel))
                #vc = await client.join_voice_channel(voice_channel)
                #player = await vc.create_ytdl_player(url, after=lambda: ## TODO: Function to run)
                #players[server.id] = player
                #player.start()
            if command.upper().startswith("PLAYURL"):
                url = command[8:]
                voice_channel = message.author.voice_channel
                server = message.server
                if voice_channel == None:
                    await client.send_message(message.channel, "You don't seem to be connected to any voice channel")
                    return
                # Join voice channel create a player add it to
                vc = await client.join_voice_channel(voice_channel)
                player = await vc.create_ytdl_player(url)
                players[server.id] = player
                await client.send_message(message.channel, "Playing song provided in url in {} voice channel".format(voice_channel))
                player.start()
            if command.upper().startswith("PAUSE"):
                id = message.server.id
                players[id].pause()
            if command.upper().startswith("STOPMUSIC"):
                id = message.server.id
                players[id].stop()
            if command.upper().startswith("RESUME"):
                id = message.server.id
                players[id].resume()
            if command.upper().startswith("CLOSE"):
                await client.logout()
            if command.upper().startswith("DISCONNECT"):
                server = message.server
                vc = client.voice_client_in(server)
                print("disconnecting")
                await vc.disconnect()
            if command.upper().startswith("SHOWPLAYLIST"):
                playlist = readPlaylist(playListFolder)
                for item in playlist:
                    await client.send_message(message.channel, "```Found: {}```".format(item))


        else:
            await client.send_message(message.channel , "You do not have permissions to execute that")
