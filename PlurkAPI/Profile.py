# encoding: utf-8
"""
Profile.py

Created by Katharine Berry on 2009-11-20.
Copyright (c) 2009 AjaxLife Developments. All rights reserved.
"""

from Exceptions import *

class Profile(object):
    def __init__(self, api):
        self.api = api
        
    def get_own_profile(self):
        if not api.logged_in:
            raise PlurkNotLoggedIn
        return self.api.request_api('Profile', 'getOwnProfile')
    
    def get_public_profile(self, user_id=None):
        if user_id is None:
            raise PlurkMissingArgument, "user_id"
        return self.api.request_api('Profile', 'getPublicProfile')
    
