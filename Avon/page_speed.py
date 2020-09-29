from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
import requests
from oauth2client import file, client, tools

service = build('pagespeedonline', 'v4', developerKey = speed_api )

def check_page_speed(page):
  service.runpagespeed(url=page, utm_campaign=None, screenshot=None, locale=None, rule=None, snapshots=None, strategy=None, filter_third_party_resources=None, utm_source=None)


# check_page_speed("google.com")
