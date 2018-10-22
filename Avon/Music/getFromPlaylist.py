import json

playListFolder = "Avon/Music/Playlist.json"

def show_all_artists(location=playListFolder):
    with open(location, "r") as f:
        data = json.load(f)
        langs = [item for item in data]
        artists = []
        for lang in langs:
            for index, item in enumerate(data[lang]):
                artists.append(item)
        print(artists)
        return artists

def show_all_langs(location=playListFolder):
    with open(location, "r") as f:
        data = json.load(f)
        langs = [item for item in data]
        return langs

def read_playlist(location=playListFolder):
    with open(location, "r") as f:
        data = json.load(f)
        langs = [item for item in data]
        names_and_urls = {}
        for lang in langs:
            for _, item in enumerate(data[lang]):
                songs_per_artist = data[lang][item]
                print("HERE ==== ", songs_per_artist)
                for i in range(len(songs_per_artist)):
                    songName = songs_per_artist[i]["Name"]
                    url = songs_per_artist[i]["url"]
                    names_and_urls[songName] = url
        return names_and_urls

def find_by_lang(lang, location=playListFolder):
    with open(location, "r") as f:
        data = json.load(f)
        names_and_urls = {}
        langs = [item for item in data]
        lang = lang.upper()
        if lang.upper() in langs:
            for _, item in enumerate(data[lang]):
                songs_per_artist = data[lang][item]
                for i in range(len(songs_per_artist)):
                    song_name = songs_per_artist[i]["Name"]
                    url = songs_per_artist[i]["url"]
                    names_and_urls[song_name] = url
            return names_and_urls
        else:
            return {"Error": "Couldn't find {} language".format(lang)}

def find_by_artist(artist, location=playListFolder):
    with open(location, "r") as f:
        data = json.load(f)
        names_and_urls = {}
        langs = [item for item in data]
        for lang in langs:
            artist_keys = [artist.upper() for artist in data[lang].keys()]
            if artist.upper() in artist_keys:
                songs_per_artist = data[lang][artist.title()]
                for i in range(len(songs_per_artist)):
                    song_name = songs_per_artist[i]["Name"]
                    url = songs_per_artist[i]["url"]
                    names_and_urls[song_name] = url
        if len(names_and_urls) == 0:
            return {"Error": "No artist named {} found".format(artist)}
        else:
            return names_and_urls
