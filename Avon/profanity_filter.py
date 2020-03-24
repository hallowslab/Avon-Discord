import requests
import json
from urllib import request,parse
from Avon.api_key import neutrino_api_uid, neutrino_api_key

async def filter_messages(message, client):
  if message.author == client.user or message.content.startswith("!"):
    return
  filter_url = "https://neutrinoapi.net/bad-word-filter"
  payload  = {"user-id": neutrino_api_uid,
             "api-key": neutrino_api_key,
             "content": message.content}
  r = requests.get(filter_url, params=payload)
  if r.status_code == 400:
    if r.json()["api-error"] == 2:
      print("DAILY API LIMIT EXCEEDED")
      return
  if r.json()["is-bad"] == True:
    await message.channel.send("Watch your profanity")
    await message.delete()