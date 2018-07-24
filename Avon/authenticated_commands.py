from api_key import master_id
from api_key import page_speed
import json


Music_channel = "446734255561900056"
playListFolder = "Avon/Music/Playlist.json"

def readPlaylist(location):
    with open(location, "r") as f:
        data = json.load(f)
        return data


async def Commands(message, client):
    if message.content.startswith("!"):
        if message.author.id == master_id:
            command = message.content[1:]
            if command.upper().startswith("TESTSPEED"):
                await client.send_message(message.channel, "Testing speed")
            elif command.upper().startswith("PLAY"):
                args = command[5:]
            elif command.upper().startswith("CLOSE"):
                await client.logout()
            else:
                await client.send_message(message.channel, "Command not recognized, or not implemented...")
        else:
            await client.send_message(message.channel , "You do not have permissions to execute that")
