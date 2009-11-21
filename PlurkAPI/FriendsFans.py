# encoding: utf-8
"""
FriendsFans.py

Created by Katharine Berry on 2009-11-21.
Copyright (c) 2009 AjaxLife Developments. All rights reserved.
"""

class FriendsFans(object):
    def __init__(self, api):
        self.api = api
    
    def get_friends_by_offset(self, user_id=None, offset=None):
        raise NotImplemented
    
    def get_fans_by_offset(self, user_id=None, offset=None):
        raise NotImplemented
    
    def get_following_by_offset(self, offset=None):
        raise NotImplemented
    
    def become_friend(self, friend_id=None):
        raise NotImplemented
    
    def remove_as_friend(self, friend_id=None):
        raise NotImplemented
    
    def become_fan(self, fan_id=None):
        raise NotImplemented
    
    def set_following(self, user_id=None, follow=None):
        raise NotImplemented
    
    def get_completion(self):
        raise NotImplemented
