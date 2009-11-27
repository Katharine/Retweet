# encoding: utf-8
"""
Responses.py

Created by Katharine Berry on 2009-11-21.
Copyright (c) 2009 AjaxLife Developments. All rights reserved.
"""

import Utilities
from Exceptions import *
from Models import *

class Responses(object):
    def __init__(self, api):
        self.api = api
    
    def get(self, plurk_id=None, from_response=0):
        if plurk_id is None:
            raise PlurkMissingArgument, "plurk_id"
        data = self.api.request_api('Responses', 'get', plurk_id=Utilities.normalise_plurk_id(plurk_id), from_response=from_response)
        friends = {}
        for friend in data['friends']:
            friends[int(friend)] = User(data['friends'][friend])
        responses_seen = data['responses_seen']
        responses = []
        for response in data['responses']:
            responses.append(Response(response))
        return friends, responses, responses_seen
    
    def response_add(self, plurk_id=None, content=None, qualifier=':'):
        if not self.api.logged_in:
            raise PlurkNotLoggedIn
        if plurk_id is None:
            raise PlurkMissingArgument, "plurk_id"
        if content is None:
            raise PlurkMissingArgument, "content"
        try:
            return Response(self.api.request_api('Responses', 'responseAdd', plurk_id=Utilities.normalise_plurk_id(plurk_id), content=content, qualifier=qualifier))
        except TypeError, ValueError:
            raise PlurkInvalidArgument, "plurk_id"
    
    def response_delete(self, plurk_id=None, response_id=None):
        raise NotImplemented
    
    add = response_add
    delete = response_delete
