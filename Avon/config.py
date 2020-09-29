import json

access_keys = {}

def load_keys(store=access_keys):
  print("Loading keys")
  with open("Avon/api_keys.json") as j_file:
    store = json.load(j_file)
    for API in store:
      access_keys.update({API: store[API]})
    
