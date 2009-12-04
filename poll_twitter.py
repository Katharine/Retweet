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
    SELECT id, plurk_uid, plurk_nick, twitter_nick, twitter_key, twitter_secret,
           last_tweet, last_mention, last_dm, enable_home, enable_mention, enable_dm
    FROM users
    WHERE enabled = 1
    """
)

rows = c.fetchall()
for row in rows:
    user_id, plurk_uid, plurk_nick, twitter_nick, twitter_key, twitter_secret, \
        last_tweet, last_mention, last_dm, enable_home, enable_mention, enable_dm = row
    oauth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET, config.TWITTER_CALLBACK_URL)
    oauth.set_access_token(twitter_key, twitter_secret)
    
    twitter_api = tweepy.API(oauth)
    all_tweets = []
    if enable_home:
        all_home = twitter_api.home_timeline(since_id=last_tweet, count=10)
        all_tweets.extend(all_home) # Count could be 200, but then we'd spam 200 plurks.
        if len(all_home) > 0:
            c.execute("UPDATE users SET last_tweet = %s WHERE id = %s", (all_home[0].id, user_id))
        print "Polled home - %s" % len(all_tweets)
    if enable_mention:
        all_mention = twitter_api.mentions(since_id=last_mention, count=10)
        all_tweets.extend(all_mention)
        if len(all_mention) > 0:
            c.execute("UPDATE users SET last_mention = %s WHERE id = %s", (all_mention[0].id, user_id))
        print "Polled mentions - %s" % len(all_tweets)
    if enable_dm:
        all_dm = twitter_api.direct_messages(since_id=last_dm, count=10)
        all_tweets.extend(all_dm)
        if len(all_dm) > 0:
            c.execute("UPDATE users SET last_dm = %s WHERE id = %s", (all_dm[0].id, user_id))
        print "Polled DMs - %s" % len(all_tweets)
    new_tweets = []
    
    for tweet in all_tweets:
        inserted = False
        for i in xrange(0, len(new_tweets)):
            if new_tweets[i].id == tweet.id:
                inserted = True
                break
            if new_tweets[i].id > tweet.id:
                new_tweets.insert(i, tweet)
                inserted = True
                break
        if not inserted:
            new_tweets.append(tweet)
    
    
    if len(new_tweets) == 0:
        continue
    
    #new_tweets.reverse()
    for tweet in new_tweets:
        c.execute("SELECT plurk FROM plurkedtweets WHERE tweet = %s", tweet.id)
        if c.fetchone() is not None:
            continue
        is_dm = isinstance(tweet, tweepy.DirectMessage)
        if is_dm:
            print "Got a DM"
            tweet.author = tweet.sender
            c.execute("""SELECT plurk FROM plurkedtweets WHERE 
                tweeter = %s AND is_dm = 1 AND userid = %s AND `date` > DATE_SUB(NOW(), INTERVAL 1 DAY)""",
                (tweet.author.screen_name, user_id)
            )
            in_reply_to_plurk = c.fetchone()
            if in_reply_to_plurk:
                in_reply_to_plurk = in_reply_to_plurk[0]
            else:
                in_reply_to_plurk = None
        else:
            if tweet.in_reply_to_status_id:
                c.execute("SELECT plurk FROM plurkedtweets WHERE tweet = %s", tweet.in_reply_to_status_id)
                in_reply_to_plurk = c.fetchone()
                if in_reply_to_plurk:
                    in_reply_to_plurk = in_reply_to_plurk[0]
                    print "Replying to plurk #%s" % in_reply_to_plurk
                else:
                    in_reply_to_plurk = None
            else:
                in_reply_to_plurk = None
        plurk_text = '%s%s: %s' % ('(DM) ' if is_dm else '', tweet.author.screen_name, re.sub(r'\B@([0-9a-zA-Z_]+)', r'twitter.com/\1 (@\1)', tweet.text))
        plurk_text = plurk_text.replace('http://','') # Save on characters.
        parts = textwrap.wrap(PlurkAPI.Utilities.decode_html_entities(plurk_text).encode('utf-8'), 139)
        print parts
        try:
            if in_reply_to_plurk is None:
                reply_to = plurk_api.Timeline.plurk_add(
                    content=parts.pop(0),
                    limited_to=plurk_uid,
                    qualifier='shares'
                ).plurk_id
                print "Made new plurk"
            else:
                plurk_api.Responses.add(plurk_id=in_reply_to_plurk, qualifier='shares', content=parts.pop(0))
                reply_to = in_reply_to_plurk
                print "Reponding to old plurk #%s" % reply_to
            while len(parts) > 0:
                plurk_api.Responses.add(plurk_id=reply_to, content=('…%s' % parts.pop(0)))
    
            c.execute("""
                INSERT INTO plurkedtweets (userid, tweeter, tweet, plurk, `date`, in_reply_to, is_dm)
                VALUES (%s, %s, %s, %s, NOW(), %s, %s)""",
                (user_id, tweet.author.screen_name, tweet.id, reply_to, tweet.in_reply_to_status_id if not is_dm else None, int(is_dm))
            )
        except PlurkAPIError:
            print "Boo, error."
            pass
