#!/usr/bin/env python
# encoding: utf-8
"""
poll_twitter.py

Created by Katharine Berry on 2009-11-21.
Copyright (c) 2009 AjaxLife Developments. All rights reserved.

Polls Twitter and sends the results to Plurk
"""

import config
import PlurkAPI
import tweepy
import MySQLdb
import re
import textwrap
from PlurkAPI.Exceptions import *

plurk_api = PlurkAPI.PlurkAPI(config.API_KEY, config.PLURK_USER, config.PLURK_PASSWORD)
plurk_api.login()

link = MySQLdb.connect(passwd=config.MYSQL_PASSWORD, user=config.MYSQL_USER, db=config.MYSQL_DATABASE, host=config.MYSQL_SERVER)
c = link.cursor()

c.execute("""
    SELECT id, plurk_uid, plurk_nick, twitter_nick, twitter_key, twitter_secret, last_tweet, last_mention, last_dm
    FROM users
    WHERE enabled = 1
    """
)

rows = c.fetchall()
for row in rows:
    user_id, plurk_uid, plurk_nick, twitter_nick, twitter_key, twitter_secret, last_tweet, last_mention, last_dm = row
    oauth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET, config.TWITTER_CALLBACK_URL)
    oauth.set_access_token(twitter_key, twitter_secret)
    
    twitter_api = tweepy.API(oauth)
    new_tweets = twitter_api.home_timeline(since_id=last_tweet, count=10) # Count could be 200, but then we'd spam 200 plurks.
    if len(new_tweets) == 0:
        continue
    
    new_tweets.reverse()
    for tweet in new_tweets:
        c.execute("SELECT plurk FROM plurkedtweets WHERE tweet = %s", tweet.id)
        if c.fetchone() is not None:
            continue
        if tweet.in_reply_to_status_id:
            c.execute("SELECT plurk FROM plurkedtweets WHERE tweet = %s", tweet.in_reply_to_status_id)
            in_reply_to_plurk = c.fetchone()
            if in_reply_to_plurk:
                in_reply_to_plurk = in_reply_to_plurk[0]
                print "Replying to plurk #%s" % in_reply_to_plurk
        else:
            in_reply_to_plurk = None
        plurk_text = '%s: %s' % (tweet.author.screen_name, re.sub(r'\B@([0-9a-zA-Z_]+)', r'twitter.com/\1 (@\1)', tweet.text))
        plurk_text = plurk_text.replace('http://','') # Save on characters.
        parts = textwrap.wrap(plurk_text.encode('utf-8'), 140)
        print parts
        try:
            if in_reply_to_plurk is None:
                reply_to = plurk_api.Timeline.plurk_add(
                    content=parts.pop(0),
                    limited_to=plurk_uid
                ).plurk_id
                print "Made new plurk"
            else:
                plurk_api.Responses.add(plurk_id=in_reply_to_plurk, qualifier='says', content=parts.pop(0))
                reply_to = in_reply_to_plurk
                print "Reponding to old plurk #%s" % reply_to
            while len(parts) > 0:
                plurk_api.Responses.add(plurk_id=reply_to, qualifier='says', content=parts.pop(0))
    
            c.execute("""
                INSERT INTO plurkedtweets (userid, tweeter, tweet, plurk, `date`, in_reply_to)
                VALUES (%s, %s, %s, %s, NOW(), %s)""",
                (user_id, tweet.author.screen_name, tweet.id, reply_to, tweet.in_reply_to_status_id)
            )
        except PlurkAPIError:
            print "Boo, error."
            pass
    
    c.execute("UPDATE users SET last_tweet = %s WHERE id = %s", (new_tweets[-1].id, user_id))