import snscrape.modules.twitter as sntwitter
import pandas as pd
import tweepy
from clean import clean_mentions 
import time
import datetime
import os

auth = tweepy.OAuthHandler(os.environ.get('OAUTH_TOKEN'), os.environ.get('OAUTH_SECRET'))
auth.set_access_token(os.environ.get('ACCESS_TOKEN'), os.environ.get("ACCESS_SECRET")) # Not sure if I named them correctly ;)

api = tweepy.API(auth, wait_on_rate_limit=True)

test_data = ["@asdfa shubhpatni.eth 5 verified 7 11", "@asdfa shubhpat 5 verified 7 11"]
test_tweets = ["Drop your ENS", "drop something"]
bot_id = int(api.me().id_str)
recent_tweets = []

def look_for_mentions(mention_id):
    mentioned_texts = []    
    for mention in api.mentions_timeline(count=50, since_id=mention_id):
        mention_id = mention.id
        if mention.author.id != bot_id:
            mentioned_texts.append({"text":mention.text, 
                                    "metadata": {"id": mention.id, "username": mention.author.screen_name}})
            
    return mentioned_texts, mention_id

def reply(cleaned_data, metadata):
    for each in zip(cleaned_data, metadata):
        print(each)
        if each[0][0] != "ERROR":
            try:
                print(post_reply(each[0][0],each[0][1], each[0][2], each[0][3], each[0][4]))
            except Exception as exc:
                print("ERROR - {}".format(exc))
        else:
            reply_with_error(each[1]["id"], each[1]["username"])
            print("Replied With Error")

def reply_with_error(id, username):
    api.update_status("@{} Fam, I guess you missed something, check this out to learn how to use the bot - https://twitter.com/dropmyENS/status/1482133543232757764?s=20".format(username), 
    in_reply_to_status_id=id, auto_populate_reply_metadata=True)

def post_reply(ens, num_of_replies, is_verified, like_count, retweet_count):
    tweets_data = get_tweets_ids(num_of_replies, is_verified, like_count, retweet_count)
    for each in tweets_data:
        try:
            print("replied to {} with id: {}".format(each['username'],each["id"]))
            api.update_status("Gm @{}, Here you go- {}".format(each["username"], ens), in_reply_to_status_id=each["id"], auto_populate_reply_metadata=True)
        except Exception as exc:
            return exc
    return "Success"

def get_tweets_ids(num_of_replies, is_verified, like_count, retweet_count):
    tweets_ids = []
    # Using TwitterSearchScraper to scrape data and append tweets to list
    until = datetime.datetime.now().strftime("%Y-%m-%d")
    since = datetime.datetime.now() - datetime.timedelta(hours = 23)
    since = since.strftime("%Y-%m-%d")

    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'drop your ENS -likeCount:{like_count} -retweetCount:{retweet_count} since:{since} until:{until}').get_items()):
        if i>num_of_replies:
            break
        tweets_ids.append({"id": tweet.id, "username":tweet.user.username})
        
    return tweets_ids

def __main__():
    while True:
        mention_id = 0
        with open("latest_mention.txt", "r+") as f:
            mention_id = f.readlines()[0]

        data, mention_id = look_for_mentions(mention_id)
        
        if data:            
            texts = [i["text"] for i in data]
            metadata = [i["metadata"] for i in data]

            print("TEXTS - ", texts)
            print("METADATA - ", metadata)

            cleaned_data = clean_mentions(texts)
            reply(cleaned_data, metadata)
        else:
            print("No more mentions")
        
        with open("latest_mention.txt", "w+") as f:
            f.write(mention_id)

        time.sleep(60)


__main__()




