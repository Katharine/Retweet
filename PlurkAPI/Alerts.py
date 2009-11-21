# encoding: utf-8
"""
Alerts.py

Created by Katharine Berry on 2009-11-21.
Copyright (c) 2009 AjaxLife Developments. All rights reserved.
"""

class Alerts(object):
    def __init__(self, api):
        self.api = api
    
    def get_active(self):
        raise NotImplemented
    
    def get_history(self):
        raise NotImplemented
    
    def add_as_fan(self, user_id):
        raise NotImplemented
    
    def add_as_friend(self, user_id):
        raise NotImplemented
    
    def add_all_as_fan(self):
        raise NotImplemented
    
    def add_all_as_friends(self):
        raise NotImplemented
    
    def deny_friendship(self):
        raise NotImplemented
    
    def remove_notification(self):
        raise NotImplemented
    
