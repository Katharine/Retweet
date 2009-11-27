#!/usr/bin/env python
# encoding: utf-8
"""
Models.py

Created by Katharine Berry on 2009-11-21.
Copyright (c) 2009 AjaxLife Developments. All rights reserved.
"""

import Utilities

class User(object):
    GENDER_MALE = 1
    GENDER_FEMALE = 0
    
    def __init__(self, dic):
        self.display_name = dic['display_name'] if 'display_name' in dic else dic['nick_name']
        self.nick_name = dic['nick_name']
        self.has_profile_image = dic['has_profile_image'] if 'has_profile_image' in dic else None
        self.date_of_birth = Utilities.parse_time(dic['date_of_birth']) if 'date_of_birth' in dic else None
        self.location = dic['location'] if 'location' in dic else None
        self.full_name = dic['full_name'] if 'full_name' in dic else self.display_name
        self.gender = dic['gender'] if 'gender' in dic else None
        self.timezone = dic['timezone'] if 'timezone' in dic else None
        self.karma = dic['karma'] if 'karma' in dic else None
        self.id = dic['id'] if 'id' in dic else None
        self.avatar = dic['avatar'] if 'avatar' in dic else None

class Plurk(object):
    """Represents an individual plurk"""
    def __init__(self, dic):
        self.plurk_id = dic['plurk_id']
        self.id = self.plurk_id
        self.qualifier = dic['qualifier']
        self.qualifier_translated = dic['qualifier_translated'] if 'qualifier_translated' in dic else self.qualifier
        self.is_unread = dic['is_unread']
        self.plurk_type = dic['plurk_type'] if 'plurk_type' in dic else None
        self.user_id = dic['user_id'] if 'user_id' in dic else None
        self.owner_id = dic['owner_id'] if 'owner_id' in dic else None
        self.posted = Utilities.parse_time(dic['posted']) if 'posted' in dic else None
        self.no_comments = dic['no_comments']
        self.content = dic['content']
        self.content_raw = dic['content_raw'] if 'content_raw' in dic else None
        self.response_count = dic['response_count']
        self.responses_seen = dic['responses_seen']
        if 'limited_to' in dic and dic['limited_to'] is not None:
            self.limited_to = dic['limited_to'].strip('|').split('||')
        else:
            self.limited_to = None

class Response(object):
    """Represents a response to a plurk"""
    
    #{u'lang': u'en', u'content_raw': u'(unsure)', u'user_id': 723933, u'qualifier': u'says', u'plurk_id': 168230297, u'content': u'<img src="http://statics.plurk.com/6cb1dc388b9259565efedef8f336d27d.gif" class="emoticon" alt="(unsure)" height="18" />', u'id': 761321462, u'posted': u'Fri, 27 Nov 2009 15:14:22 GMT'}}
    def __init__(self, dic):
        self.lang = dic['lang']
        self.content_raw = dic['content_raw']
        self.user_id = dic['user_id']
        self.qualifier = dic['qualifier']
        self.qualifier_translated = dic['qualifier_translated'] if 'qualifier_translated' in dic else self.qualifier
        self.plurk_id = dic['plurk_id']
        self.content = dic['content']
        self.id = dic['id']
        self.posted = Utilities.parse_time(dic['posted'])