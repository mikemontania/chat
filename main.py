# main.py

from reddit_client import connect_reddit
from scraper import scrape_subreddit
from config import SUBREDDITS_LIMIT

def main():
    reddit = connect_reddit()
    subreddits = reddit.subreddits.popular(limit=SUBREDDITS_LIMIT)

    for subreddit in subreddits:
        scrape_subreddit(subreddit)

if __name__ == "__main__":
    main()
