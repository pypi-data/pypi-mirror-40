import praw
import requests
from . import config


def make_client(user_agent):
    return praw.Reddit(
        user_agent=user_agent,
        client_id=config.client_id,
        client_secret=config.client_secret,
    )

COMMENT_MESSAGE_FMT = """
.

New [comment!](<{url}>)

"{body}"

- {author} 
in "{submission_title}"
"""


def monitor_comments():
    reddit = make_client(user_agent='Expanse Latest Comments to Discord Bot')
    for comment in reddit.subreddit(config.subreddit).stream.comments(skip_existing=True):
        print("comment received: ", comment)
        url = "https://www.reddit.com{}?context=9&depth=8".format(comment.permalink)
        content = COMMENT_MESSAGE_FMT.format(url=url, author=comment.author, body=comment.body, submission_title=comment.submission.title)
        data = {
            "content": content,
        }
        requests.post(config.discord_webhook, data=data)


SUBMISSION_MESSAGE_FMT = """
New [submission!](<{url}>)

"{title}"

- {author} 
"""

def monitor_submissions():
    reddit = make_client(user_agent='Expanse Latest Submissions to Discord Bot')
    for submission in reddit.subreddit(config.subreddit).stream.submissions(skip_existing=True):
        print("submission received: ", submission)

        url = "https://www.reddit.com{}".format(submission.permalink)
        content = SUBMISSION_MESSAGE_FMT.format(url=url, author=submission.author, title=submission.title)

        data = {
            "content": content,
        }
        requests.post(config.discord_webhook, data=data)

