import json

playListFolder = "Avon/Music/Playlist.json"

def showAllArtists(location=playListFolder):
    with open(location, "r") as f:
        data = json.load(f)
        genres = []
        artists = []
        for item in data:
            genres.append(item)
        for genre in genres:
            for index, item in enumerate(data[genre][0]):
                artists.append(genre + " - " + item)
        return artists

def showAllGenres(location=playListFolder):
    with open(location, "r") as f:
        data = json.load(f)
        genres = []
        for item in data:
            genres.append(item)
        return genres

def readPlaylist(location=playListFolder):
    with open(location, "r") as f:
        data = json.load(f)
        genres = []
        namesAndUrls = {}
        for item in data:
            genres.append(item)
        for genre in genres:
            for index, item in enumerate(data[genre][0]):
                currentArtist = item
                songsPerArtist = data[genre][0][item]
                for i in range(len(songsPerArtist)):
                    songName = songsPerArtist[i]["Name"]
                    url = songsPerArtist[i]["url"]
                    namesAndUrls[songName] = url
        print(namesAndUrls)
        # for index, item in enumerate(Tuga_all):
        #     currentArtist = Tuga_all[item]
        #     for i in range(len(currentArtist)):
        #         url = currentArtist[i]["url"]
        #         songName = currentArtist[i]["Name"]
        #         yield(songName, url)

def findByGenre(genre, location=playListFolder):
    with open(location, "r") as f:
        data = json.load(f)
        if genre.upper() == "TUGA" or genre.upper() == "PORTUGUES":
            #Return Tuga music Playlist
            pass
        elif genre.upper() == "ENGLISH" or genre.upper() == "ENG":
            #Return english music playlist
            pass


readPlaylist("Avon/Music/Playlist.json")
