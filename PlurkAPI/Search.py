#!/usr/bin/env python
# encoding: utf-8
"""
Search.py

Created by Katharine Berry on 2009-11-21.
Copyright (c) 2009 AjaxLife Developments. All rights reserved.
"""

class Search(object):
    def __init__(self, api):
        self.api = api
    
    def plurk_search(self, query):
        raise NotImplemented
    
    def user_search(self, query):
        raise NotImplemented
    
