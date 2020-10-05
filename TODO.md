#### Avon.extensions.music_commands

```
# Disconnects from the voice channel
# TODO: This should disconnect when the music finishes
# since stop music already disconnects and cleans up the player
if command.upper().startswith("DISCONNECT"):
    MUSIC_PLAYER.stop()
    MUSIC_PLAYER = None
    voice_channel = client.get_channel(config.access_keys["music_channel_id"])
    await message.channel.send("Disconnecting")
    await voice_channel.disconnect()
    await voice_channel.cleanup()
```

```
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
```

```
# # TODO: Create function for queueing songs
if command.upper().startswith("PLAY"):
    Playlist = command[5:]
    voice_channel = message.author.voice_channel
    server = message.server
    if voice_channel == None:
        await message.channel.send("You don't seem to be connected to any voice channel")
        return
    await message.channel.send("Playing song provided in \
                               url in {} voice channel".format(voice_channel))
    vc = await client.join_voice_channel(voice_channel)
    player = await vc.create_ytdl_player(url, after=lambda: ## FIXME: Function to run)
    players[server.id] = player
    player.start()
    # The function to run after might need something like this
    #start = time.time()
    #time.clock()
    #elapsed = 0
    #while elapsed < player.duration:
    #    elapsed = time.time() - start
    #print("Song playing")
    #if elapsed > player.duration:
    #    print("Song Finished")
    #    return
```