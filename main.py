"""
A simple command line utility to do sentiment analysis on a sub-reddit
This tries to predict the total positive, negative and neutral posts in a given time frame.
NOTE: This does not do apply advanced learning models but relies on the text-processing service for the prediction &
is intended to be for educational purposes.
"""
import praw
import requests
import argparse
from config import Config


def do_sentiment_analysis(subreddit_name, time_filter):
    """
    Do sentiment analysis on a sub-reddit
    :param subreddit_name:
    :param time_filter:
    :return:
    """
    reddit_config = Config()

    reddit = praw.Reddit(client_id=reddit_config.get_client_id(),
                         client_secret=reddit_config.get_client_secret(),
                         user_agent='USERAGENT')

    all_submissions = reddit.subreddit(subreddit_name).top(time_filter=time_filter)
    SENTIMENT_PROCESSING_API = 'http://text-processing.com/api/sentiment/'

    pos_count = 0
    neg_count = 0
    neu_count = 0
    total_posts = 0

    for submission in all_submissions:
        total_posts += 1
        try:
            payload = {'text': submission.title}
            r = requests.post(SENTIMENT_PROCESSING_API, data=payload)
            sentiment = r.json().get('label')
            if sentiment == 'pos':
                pos_count += 1
            elif sentiment == 'neg':
                neg_count += 1
            else:
                neu_count += 1
        except:
            raise

    # Color formatters
    formatters = {
        'RED': '\033[91m',
        'GREEN': '\033[92m',
        'GREY': '\33[90m',
        'END': '\033[0m',
    }

    print "Total posts scanned: {} ".format(total_posts)
    print "{GREEN} Positive comments:  {} {END}".format(pos_count, **formatters)
    print "{RED} Negative comments:  {} {END}".format(neg_count, **formatters)
    print "{GREY} Neutral comments:  {} {END}".format(neu_count, **formatters)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--subreddit_name",
                        help="Name of the sub-reddit to scan",
                        required=True)
    parser.add_argument("-t", "--time_filter",
                        help="Time period to scan ",
                        choices=['all', 'day', 'hour', 'month', 'week', 'year'],
                        default='day')
    args = parser.parse_args()

    do_sentiment_analysis(args.subreddit_name, args.time_filter)



