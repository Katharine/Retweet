#!/usr/bin/env python
# encoding: utf-8
"""
poll_alerts.py

Created by Katharine Berry on 2009-11-21.
Copyright (c) 2009 AjaxLife Developments. All rights reserved.

Polls for any new friend requests and accepts them.
"""

import config
import PlurkAPI
import tweepy
import MySQLdb

api = PlurkAPI.PlurkAPI(config.API_KEY, config.PLURK_USER, config.PLURK_PASSWORD)
api.login()
alerts = api.Alerts.get_active()

if len(alerts) == 0:
    print "No new friends. :("
    exit()

# Be ready to do OAuth and MySQL stuff
link = MySQLdb.connect(passwd=config.MYSQL_PASSWORD, user=config.MYSQL_USER, db=config.MYSQL_DATABASE, host=config.MYSQL_SERVER)
c = link.cursor()

for alert in alerts:
    if isinstance(alert, PlurkAPI.Alerts.FriendshipRequest):
        user = alert.from_user
        oauth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET, config.TWITTER_CALLBACK_URL)
        url = oauth.get_authorization_url()
        api.Alerts.add_as_friend(user.id)
        api.Timeline.plurk_add(
            qualifier='says',
            content='Thank you for using Twitterbot. To complete setup, click %s (here).' % url,
            limited_to=user.id,
            no_comments=1
        )
        c.execute("""
            REPLACE INTO pending (plurk_uid, plurk_nick, twitter_key, twitter_secret, signup_time)
            VALUES (%s, %s, %s, %s, NOW())
        """, (user.id, user.nick_name, oauth.request_token.key, oauth.request_token.secret))
        
        print "Friend request from %s (%s) - URL: %s." % (user.full_name.encode('utf-8'), user.nick_name, url)

c.close()
link.close()