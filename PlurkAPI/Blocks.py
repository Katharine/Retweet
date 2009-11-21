# encoding: utf-8
"""
Blocks.py

Created by Katharine Berry on 2009-11-21.
Copyright (c) 2009 AjaxLife Developments. All rights reserved.
"""

class Blocks(object):
    def __init__(self, api):
        self.api = api
    
    def get(self, offset=None):
        raise NotImplemented
    
    def block(self, user_id=None):
        raise NotImplemented
    
    def unblock(self, user_id=None):
        raise NotImplemented