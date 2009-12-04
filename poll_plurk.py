#!/usr/bin/env python
# encoding: utf-8
"""
poll_plurk.py

Created by Katharine Berry on 2009-11-21.
Copyright (c) 2009 AjaxLife Developments. All rights reserved.
"""

import config
import PlurkAPI
import re
import MySQLdb
import tweepy

plurk_api = PlurkAPI.PlurkAPI(config.API_KEY, config.PLURK_USER, config.PLURK_PASSWORD)
plurk_api.login()

# MySQL init
link = MySQLdb.connect(passwd=config.MYSQL_PASSWORD, user=config.MYSQL_USER, db=config.MYSQL_DATABASE, host=config.MYSQL_SERVER)
c = link.cursor()

# Titter init
oauth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET, config.TWITTER_CALLBACK_URL)

unread = plurk_api.Timeline.get_unread_plurks()
to_mute = []
for plurk in unread:
    print plurk.limited_to
    if plurk.limited_to is not None and len(plurk.limited_to) == 2:
        friends, responses, responses_seen = plurk_api.Responses.get(plurk)
        replies = responses[responses_seen:]
        for reply in replies:
            if reply.user_id == plurk_api.user_id:
                print "My own reply, aborting"
                continue
            c.execute("SELECT tweeter, tweet, in_reply_to, userid, is_dm FROM plurkedtweets WHERE plurk = %s ORDER BY tweet ASC LIMIT 1", plurk.id)
            tweetdata = c.fetchone()
            if tweetdata is None:
                print "Couldn't get any data about the plurk"
                continue
            tweeter, tweet, in_reply_to, user_id, is_dm = tweetdata
            c.execute("SELECT twitter_key, twitter_secret, twitter_nick FROM users WHERE id = %s", user_id)
            twitterlogin = c.fetchone()
            if twitterlogin is None:
                print "Couldn't get Twitter login details."
                continue
            twitter_key, twitter_secret, twitter_nick = twitterlogin
            oauth.set_access_token(twitter_key, twitter_secret)
            twitter_api = tweepy.API(oauth)
            
            tweet_text = reply.content_raw
            if not is_dm:
                reply_to_nick = re.match('@([0-9a-zA-Z_]+)', tweet_text)
                reply_to_id = tweet
                if reply_to_nick is None:
                    reply_to_nick = tweeter
                else:
                    reply_to_nick = reply_to_nick.group(1)
                    tweet_text = tweet_text[len(reply_to_nick) + 2:]
            
                c.execute("SELECT tweeter, tweet FROM plurkedtweets WHERE plurk = %s AND tweeter = %s ORDER BY tweet DESC LIMIT 1", (plurk.id, reply_to_nick))
                reply_to_data = c.fetchone()
                if reply_to_data is None:
                    c.execute("SELECT tweeter, tweet FROM plurkedtweets WHERE plurk = %s AND tweeter = %s ORDER BY tweet DESC LIMIT 1", (plurk.id, tweeter))
                    reply_to_nick, reply_to_id = c.fetchone()
                else:
                    reply_to_nick, reply_to_id = reply_to_data
            
                tweet_text = ("@%s %s" % (reply_to_nick, tweet_text))[:140]
            
                status = twitter_api.update_status(status=tweet_text, in_reply_to_status_id=reply_to_id)
            else:
                status = twitter_api.send_direct_message(user=tweeter, text=tweet_text[:140])
                reply_to_id = None
            c.execute("""INSERT INTO
                plurkedtweets (userid, tweeter, tweet, plurk, `date`, in_reply_to, is_dm)
                VALUES (%s, %s, %s, %s, NOW(), %s, %s)""",
                (user_id, twitter_nick, status.id, plurk.id, reply_to_id, int(is_dm))
            )
            print "Tweeted tweet %s \"%s\" in reply to %s for %s" % (status.id, tweet_text, reply_to_id, user_id)
    else:
        to_mute.append(plurk.plurk_id)

print "Muting %s." % to_mute
plurk_api.Timeline.mute_plurks(to_mute)