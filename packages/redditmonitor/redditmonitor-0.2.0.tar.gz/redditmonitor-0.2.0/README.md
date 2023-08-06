Set the following environment variables to run:
* CLIENT_ID
* CLIENT_SECRET
* USERNAME
* PASSWORD
* DISCORD_WEBHOOK
* SUBREDDIT

The following entrypoints are available
* monitor_comments - looks for new comments and posts them to the discord webhook
* monitor_submissions - looks for new submissions and posts them to the discord webhook

### Example Running

```sh
CLIENT_ID='CLIENT_ID' \
CLIENT_SECRET='CLIENT_SECRET' \
REDDIT_PASSWORD='REDDIT_PASSWORD' \
REDDIT_USERNAME='REDDIT_USERNAME' \
SUBREDDIT='worldnews' \
DISCORD_WEBHOOK='https://discordapp.com/api/webhooks/{ID}/{SECRET_TOKEN}' \
monitor_comments
```
