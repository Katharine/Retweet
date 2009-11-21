# encoding: utf-8
"""
Responses.py

Created by Katharine Berry on 2009-11-21.
Copyright (c) 2009 AjaxLife Developments. All rights reserved.
"""

class Responses(object):
    def __init__(self, api):
        self.api = api
    
    def get(self, plurk_id=None, from_response=None):
        raise NotImplemented
    
    def response_add(self, plurk_id=None, content=None, qualifier=None):
        raise NotImplemented
    
    def response_delete(self, plurk_id=None, response_id=None):
        raise NotImplemented
    
    add = response_add
    delete = response_delete
