# encoding: utf-8
"""
Timeline.py

Created by Katharine Berry on 2009-11-20.
Copyright (c) 2009 AjaxLife Developments. All rights reserved.
"""

from Exceptions import *
from Models import *
import Utilities
import Users

class Timeline(object):
    def __init__(self, api):
        self.api = api
    
    def get_plurk(self, plurk_id=None):
        if plurk_id is None:
            raise PlurkMissingArgument, 'plurk_id'
        try:
            plurk_id = Utilities.normalise_plurk_id(plurk_id)
        except ValueError, TypeError:
            raise PlurkInvalidArgument, "plurk_id"
        
        if not self.api.logged_in:
            raise PlurkNotLoggedIn
        
        returned = self.api.request_api('Timeline', 'getPlurk', plurk_id=plurk_id)
        return (Plurk(returned["plurks"]), User(returned["user"]))
    
    def get_plurks(self, offset=None, limit=None, only_user=None, only_responded=False, only_private=False):
        if not self.api.logged_in:
            raise PlurkNotLoggedIn
        
        args = {}
        if offset is not None:
            try:
                args['offset'] = Utilities.normalise_offset(offset)
            except ValueError:
                raise PlurkInvalidArgument, "offset"
            
        if limit is not None:
            try:
                args['limit'] = int(limit)
            except ValueError, TypeError:
                raise PlurkInvalidArgument, "limit"
        
        if only_user is not None:
            try:
                args['only_user'] = int(only_user)
            except ValueError, TypeError:
                raise PlurkInvalidArgument, "only_user"
        
        if only_responded:
            args['only_responded'] = True
        
        if only_private:
            args['only_private'] = True
        
        returned = self.api.request_api('Timeline', 'getPlurks', **args)
        return (Utilities.parse_plurk_list(returned["plurks"]), Utilities.parse_user_list(returned["plurk_users"]))
    
    def poll(self, offset):
        if not self.api.logged_in:
            raise PlurkNotLoggedIn
        
        if offset is None:
            raise PlurkMissingArgument, "offset"
        
        try:
            returned = self.api.request_api('Polling', 'getPlurks', offset=Utilities.normalise_offset(offset))
            return (Utilities.parse_plurk_list(returned["plurks"]), Utilities.parse_user_list(returned["plurk_users"]))
        except ValueError, TypeError:
            raise PlurkInvalidArgument, "offset"
    
    def get_unread_plurks(self, offset=None, limit=None):
        if not self.api.logged_in:
            raise PlurkNotLoggedIn
        
        args = {}
        if offset is not None:
            try:
                args['offset'] = Utilities.normalise_offset(offset)
            except ValueError:
                raise PlurkInvalidArgument, "offset"
        
        if limit is not None:
            try:
                args['limit'] = int(limit)
            except ValueError, TypeError:
                raise PlurkInvalidArgument, "limit"
        
        return Utilities.parse_plurk_list(self.api.request_api('Timeline', 'getUnreadPlurks', **args)["plurks"])
    
    def mute_plurks(self, ids=None):
        if not self.api.logged_in:
            raise PlurkNotLoggedIn
        
        if ids is None:
            raise PlurkMissingArgument, "ids"
        
        try:
            self.api.request_api('Timeline', 'mutePlurks', ids=Utilities.normalise_integer_list(ids))
            return True
        except TypeError, ValueError:
            raise PlurkInvalidArgument, "ids"


    def unmute_plurks(self, ids=None):
        if not self.api.logged_in:
            raise PlurkNotLoggedIn
        if ids is None:
            raise PlurkMissingArgument, "ids"

        try:
            self.api.request_api('Timeline', 'unmutePlurks', ids=Utilities.normalise_integer_list(ids))
            return True
        except TypeError, ValueError:
            raise PlurkInvalidArgument, "ids"

    def mark_as_read(self, ids=None):
        if not self.api.logged_in:
            raise PlurkNotLoggedIn
        
        if ids is None:
            raise PlurkMissingArgument, "ids"

        try:
            self.api.request_api('Timeline', 'markAsRead', ids=Utilities.normalise_integer_list(ids))
            return True
        except TypeError, ValueError:
            raise PlurkInvalidArgument, "ids"
    
    def plurk_add(self, content=None, qualifier=':', limited_to=None, no_comments=None, lang=None):
        if not self.api.logged_in:
            raise PlurkNotLoggedIn
        
        if content is None:
            raise PlurkMissingArgument, "content"
        
        if qualifier not in Utilities.VALID_QUALIFIERS:
            raise PlurkInvalidArgument, "qualifier"
        
        args = {'content': content, 'qualifier': qualifier}
        
        if limited_to is not None:
            try:
                args['limited_to'] = Utilities.normalise_integer_list(limited_to)
            except TypeError, ValueError:
                raise PlurkInvalidArgument, "limited_to"
        
        if no_comments:
            if no_comments not in (1, 2):
                raise PlurkInvalidArgument, "no_comments"
            args['no_comments'] = no_comments
        
        if lang is not None:
            if lang not in Utilities.LANGUAGES:
                raise PlurkInvalidArgument, "lang"
            args['lang'] = lang
        
        return Plurk(self.api.request_api('Timeline', 'plurkAdd', **args))
    
    def upload_picture(self, image):
        raise NotImplemented
    
    def plurk_delete(self, plurk_id=None):
        if not self.api.logged_in:
            raise PlurkNotLoggedIn
        
        if plurk_id is None:
            raise PlurkMissingArgument, "plurk_id"
        
        try:
            self.api.request_api('Timeline', 'plurkDelete', plurk_id=Utilities.normalise_plurk_id(plurk_id))
            return True
        except ValueError, TypeError:
            raise PlurkInvalidArgument, "plurk_id"
    
    def plurk_edit(self, plurk_id=None, content=None):
        if not self.api.logged_in:
            raise PlurkNotLoggedIn
        
        if content is None:
            raise PlurkMissingArgument, "content"
        
        if plurk_id is None:
            raise PlurkMissingArgument, "plurk_id"
        
        try:
            self.api.request_api('Timeline', 'plurkEdit', plurk_id=Utilities.normalise_plurk_id(plurk_id), content=content)
            return True
        except ValueError, TypeError:
            raise PlurkInvalidArgument, "plurk_id"
    
