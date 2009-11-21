# encoding: utf-8
"""
Cliques.py

Created by Katharine Berry on 2009-11-21.
Copyright (c) 2009 AjaxLife Developments. All rights reserved.
"""

class Cliques(object):
    def __init__(self, api):
        self.api = api
    
    def get_cliques(self):
        raise NotImplemented
    
    def create_clique(self, clique_name=None):
        raise NotImplemented
    
    def get_clique(self, clique_name=None):
        raise NotImplemented
    
    def rename_clique(self, clique_name=None, new_name=None):
        raise NotImplemented
    
    def delete_clique(self, clique_name=None):
        raise NotImplemented
    
    def add(self, clique_name, user_id):
        raise NotImplemented
    
    def remove(self, clique_name, user_id):
        raise NotImplemented
    
