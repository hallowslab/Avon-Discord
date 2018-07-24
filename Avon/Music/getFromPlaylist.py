import json

def readPlaylist(location):
    with open(location, "r") as f:
        data = json.load(f)
        return data

a = readPlaylist("Avon/Music/Playlist.json")

Tuga_all = a["Tuga"][0]

for index, item in enumerate(Tuga_all):
    currentArtist = Tuga_all[item]
    for i in range(len(currentArtist)):
        url = currentArtist[i]["url"]
        songName = currentArtist[i]["Name"]
        print(songName, url)
