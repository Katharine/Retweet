#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py

Created by Katharine Berry on 2009-11-20.
Copyright (c) 2009 AjaxLife Developments. All rights reserved.
"""

import urllib
import urllib2
import cookielib
try:
    import json
except ImportError:
    import simplejson as json

# Plurk imports
from Exceptions import *
import Users
import Timeline
import Responses
import Profile
import FriendsFans
import Alerts
import Search
import Emoticons
import Blocks
import Cliques

class PlurkAPI(object):
    api_root = 'http://www.plurk.com/API/%s/%s'
    username = None
    user_id = None
    password = None
    api_key = None
    logged_in = False
    opener = None
    
    def resolve_url(self, section, command):
        return self.api_root % (section, command)
    
    def request_api(self, section, command, **args):
        args['api_key'] = self.api_key
        try:
            f = self.opener.open(self.resolve_url(section, command), urllib.urlencode(args))
            success = True
        except urllib2.HTTPError, e:
            f = e
            success = False
        data = f.read()
        try:
            decoded = json.loads(data)
        except:
            raise PlurkAPIError, "Incomprehensible response: %s" % data
        f.close()
        if 'error_text' in decoded:
            raise PlurkAPIError, decoded['error_text']
        elif not success:
            raise PlurkAPIError
        return decoded
    
    def __init__(self, key, username, password):
        self.username = username
        self.password = password
        self.api_key = key
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        
        self.Users = Users.Users(self)
        self.Timeline = Timeline.Timeline(self)
        self.Responses = Responses.Responses(self)
        self.Profile = Profile.Profile(self)
        self.FriendsFans = FriendsFans.FriendsFans(self)
        self.Alerts = Alerts.Alerts(self)
        self.Search = Search.Search(self)
        self.Emoticons = Emoticons.Emoticons(self)
        self.Blocks = Blocks.Blocks(self)
        self.Cliques = Cliques.Cliques(self)
    
    def login(self):
        try:
            response = self.request_api('Users', 'login', username=self.username, password=self.password)
            self.logged_in = True
            self.user_id = response["user_info"]["id"]
            return response
        except PlurkAPIError, e:
            return PlurkLoginError, e
    