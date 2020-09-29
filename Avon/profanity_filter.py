import requests
from Avon import config

async def filter_messages(message, client):
    """
    Checks if the message contains profanity and removes it
    """
    if message.author == client.user or message.content.startswith("!"):
        return
    filter_url = "https://neutrinoapi.net/bad-word-filter"
    payload  = {"user-id": config.access_keys["Neutrino_API_uid"],
              "api-key": config.access_keys["Neutrino_API_key"],
              "content": message.content}
    req = requests.get(filter_url, params=payload)
    if req.status_code == 400:
        if req.json()["api-error"] == 2:
            print("DAILY API LIMIT EXCEEDED")
            return
    if req.json()["is-bad"]:
        await message.channel.send("Watch your profanity")
        await message.delete()
