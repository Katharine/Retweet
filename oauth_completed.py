#!/usr/bin/env python
# encoding: utf-8
"""
oauth_completed.py

Created by Katharine Berry on 2009-11-21.
Copyright (c) 2009 AjaxLife Developments. All rights reserved.

Called by the web server when a callback arrives.
"""

import sys

import config
import PlurkAPI
import tweepy
import MySQLdb

# Plurk init
plurk = PlurkAPI.PlurkAPI(config.API_KEY, config.PLURK_USER, config.PLURK_PASSWORD)
plurk.login()

# MySQL init
link = MySQLdb.connect(passwd=config.MYSQL_PASSWORD, user=config.MYSQL_USER, db=config.MYSQL_DATABASE, host=config.MYSQL_SERVER)
c = link.cursor()

# Titter init
oauth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET, config.TWITTER_CALLBACK_URL)

c.execute("SELECT plurk_uid, plurk_nick, twitter_secret FROM pending WHERE twitter_key = %s", sys.argv[1])
user_data = c.fetchone()
oauth.set_request_token(sys.argv[1], user_data[2])
try:
    oauth.get_access_token(sys.argv[2])
except tweepy.TweepError:
    print "Failed to get access token for %s! D:" % user_data[1]
    exit()

twitter = tweepy.API(oauth)
twitter_details = twitter.me()
last_tweet = twitter_details.status.id
last_mention = twitter.mentions(count=1)
if len(last_mention) == 0:
    last_mention = 0
else:
    last_mention = last_mention[0].id
last_dm = twitter.direct_messages(count=1)
if len(last_dm) == 0:
    last_dm = 0
else:
    last_dm = last_dm[0].id
c.execute("""
    REPLACE INTO users (plurk_uid, plurk_nick, twitter_nick, twitter_key, twitter_secret, last_tweet, last_mention, last_dm, since)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())""",
    (user_data[0], user_data[1], twitter_details.screen_name, oauth.access_token.key, oauth.access_token.secret, last_tweet, last_mention, last_dm)
)
c.execute("DELETE FROM pending WHERE twitter_key = %s", sys.argv[1])
# Send a welcome plurk? 
plurk.Timeline.plurk_add(
    qualifier='says',
    content="Twitterbot is now enabled. At least, in theory. It's not fully implemented yet, really.",
    no_comments=1,
    limited_to=user_data[0]
)

c.close()
link.close()