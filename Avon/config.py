import json

access_keys = {}
settings = {}

def load_keys_and_settings():
    """
    Load api keys and settings from defined json files
    """
    with open("Avon/settings.json") as j_file:
        j_data = json.load(j_file)
        for value in j_data:
            settings.update({value: j_data[value]})
    with open("Avon/api_keys.json") as j_file:
        j_data = json.load(j_file)
        for value in j_data:
            access_keys.update({value: j_data[value]})
