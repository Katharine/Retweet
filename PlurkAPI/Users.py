# encoding: utf-8
"""
Users.py

Created by Katharine Berry on 2009-11-20.
Copyright (c) 2009 AjaxLife Developments. All rights reserved.
"""

import datetime

class Users(object):
    def __init__(self, api):
        self.api = api
    
    def register(self, nick_name=None, full_name=None, password=None, gender=None, date_of_birth=None, email=None):
        raise NotImplemented
    
    def login(self, username=None, password=None):
        if username is not None:
            self.api.username = username
        if password is not None:
            self.api.password = password
        self.api.login()
    
    def update_picture(self, profile_image=None):
        raise NotImplemented
    
    def update(self, current_password=None, full_name=None, new_password=None, email=None, display_name=None, privacy=None, date_of_birth=None):
        raise NotImplemented

class User(object):
    GENDER_MALE = 1
    GENDER_FEMALE = 0
    
    def __init__(self, dic):
        self.display_name = dic['display_name'] if 'display_name' in dic else dic['nick_name']
        self.nick_name = dic['nick_name']
        self.has_profile_image = dic['has_profile_image']
        self.date_of_birth = datetime.datetime.strptime(dic['date_of_birth'], '%a, %d %b %Y %H:%M:%S %Z').date()
        self.location = dic['location']
        self.full_name = dic['full_name']
        self.gender = dic['gender']
        self.timezone = dic['timezone']
        self.karma = dic['karma']
        self.id = dic['id']
        self.avatar = dic['avatar']