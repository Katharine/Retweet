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
        self.has_profile_image = dic['has_profile_image']
        self.date_of_birth = Utilities.parse_time(dic['date_of_birth'])
        self.location = dic['location']
        self.full_name = dic['full_name']
        self.gender = dic['gender']
        self.timezone = dic['timezone']
        self.karma = dic['karma']
        self.id = dic['id']
        self.avatar = dic['avatar']

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