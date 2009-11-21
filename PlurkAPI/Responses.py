# encoding: utf-8
"""
Responses.py

Created by Katharine Berry on 2009-11-21.
Copyright (c) 2009 AjaxLife Developments. All rights reserved.
"""

import Utilities
from Exceptions import *

class Responses(object):
    def __init__(self, api):
        self.api = api
    
    def get(self, plurk_id=None, from_response=None):
        raise NotImplemented
    
    def response_add(self, plurk_id=None, content=None, qualifier=':'):
        if plurk_id is None:
            raise PlurkMissingArgument, "plurk_id"
        if content is None:
            raise PlurkMissingArgument, "content"
        try:
            #TODO: Work out the return format of this one.
            self.api.request_api('Responses', 'responseAdd', plurk_id=Utilities.normalise_plurk_id(plurk_id), content=content, qualifier=qualifier)
        except TypeError, ValueError:
            raise PlurkInvalidArgument, "plurk_id"
    
    def response_delete(self, plurk_id=None, response_id=None):
        raise NotImplemented
    
    add = response_add
    delete = response_delete
