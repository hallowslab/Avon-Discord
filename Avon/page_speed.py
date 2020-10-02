from __future__ import print_function
from apiclient.discovery import build
from Avon import config

service = build('pagespeedonline', 'v4', developerKey = config.access_keys["page_speed"] )

def check_page_speed(page):
    """
    Runs google page speed insights
    """
    service.runpagespeed(url=page, utm_campaign=None, screenshot=None,
                         locale=None, rule=None, snapshots=None, strategy=None,
                         filter_third_party_resources=None, utm_source=None)


# check_page_speed("google.com")
