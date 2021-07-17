"""service file"""
import os

import praw

from shiversify_bot import ShiversifyBot

def main() -> None:
    reddit: praw.Reddit = praw.Reddit(
        client_id=os.environ["shiversifybot_client_id"],
        client_secret=os.environ["shiversifybot_client_secret"],
        username=os.environ["shiversifybot_username"],
        password=os.environ["shiversifybot_password"],
        user_agent="linux:shiversifybot:v1.0 (by /u/iIoveoof)"
    )

    bot: ShiversifyBot = ShiversifyBot(
        reddit,
        os.environ["shiversifybot_subreddit"]
    )

    while True:
        try:
            bot.listen()
        except Exception as e:
            print(e)


    return

if __name__ == "__main__":
    main()

