# encoding: utf-8
"""
Alerts.py

Created by Katharine Berry on 2009-11-21.
Copyright (c) 2009 AjaxLife Developments. All rights reserved.
"""

import Utilities
from Exceptions import *
from Users import User

class Alerts(object):
    def __init__(self, api):
        self.api = api
    
    def get_active(self):
        if not self.api.logged_in:
            raise PlurkNotLoggedIn
        
        return self.__process_alert_list(self.api.request_api('Alerts', 'getActive'))
    
    def get_history(self):
        if not self.api.logged_in:
            raise PlurkNotLoggedIn

        return self.__process_alert_list(self.api.request_api('Alerts', 'getHistory'))
    
    def add_as_fan(self, user_id):
        if not self.api.logged_in:
            raise PlurkNotLoggedIn

        self.api.request_api('Alerts', 'addAsFan', user_id=user_id)
    
    def add_as_friend(self, user_id):
        if not self.api.logged_in:
            raise PlurkNotLoggedIn
        
        self.api.request_api('Alerts', 'addAsFriend', user_id=user_id)
    
    def add_all_as_fan(self):
        if not self.api.logged_in:
            raise PlurkNotLoggedIn
        
        self.api.request_api('Alerts', 'addAllAsFan')
    
    def add_all_as_friends(self):
        if not self.api.logged_in:
            raise PlurkNotLoggedIn
        
        self.api.request_api('Alerts', 'addAllAsFriends')
    
    def deny_friendship(self):
        if not self.api.logged_in:
            raise PlurkNotLoggedIn
        
        self.api.request_api('Alerts', 'denyFriendship', user_id=user_id)
    
    def remove_notification(self):
        if not self.api.logged_in:
            raise PlurkNotLoggedIn
        
        self.api.request_api('Alerts', 'removeNotification', user_id=user_id)
       
    # Private
    def __process_alert_list(self, alerts):
        newlist = []
        for alert in alerts:
            t = alert['type']
            if t == 'friendship_request':
                newlist.append(FriendshipRequest(alert))
            elif t == 'friendship_pending':
                newlist.append(FriendshipPending(alert))
            elif t == 'new_fan':
                newlist.append(NewFan(alert))
            elif t == 'friendship_accepted':
                newlist.append(FriendshipAccepted(alert))
            elif t == 'new_friend':
                newlist.append(NewFriend(alert))
        
        return newlist
    
class PlurkAlert(object):
    def __init__(self, posted):
        self.posted = posted
        

class FriendshipRequest(PlurkAlert):
    def __init__(self, alert):
        self.from_user = User(alert['from_user'])
        self.posted = alert['posted']

class FriendshipPending(PlurkAlert):
    def __init__(self, alert):
        self.to_user = User(alert['to_user'])
        self.posted = alert['posted']
    
class NewFan(PlurkAlert):
    def __init__(self, alert):
        self.new_fan = User(alert['new_fan'])
        self.posted = alert['posted']
    
class NewFriend(PlurkAlert):
    def __init__(self, alert):
        self.new_friend = User(alert['new_friend'])
        self.posted = alert['posted']
    
class FriendshipAccepted(PlurkAlert):
    def __init__(self, alert):
        self.friend_info = User(alert['friend_info'])
        self.posted = alert['posted']
        