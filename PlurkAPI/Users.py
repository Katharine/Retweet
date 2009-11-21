# encoding: utf-8
"""
Users.py

Created by Katharine Berry on 2009-11-20.
Copyright (c) 2009 AjaxLife Developments. All rights reserved.
"""

import datetime
import Utilities

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
