import sys
import os

client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]
discord_webhook = os.environ["DISCORD_WEBHOOK"]
subreddit = os.environ["SUBREDDIT"]

title_filter = os.environ.get("TITLE_FILTER")