# encoding: utf-8
"""
Exceptions.py

Created by Katharine Berry on 2009-11-20.
Copyright (c) 2009 AjaxLife Developments. All rights reserved.
"""

class PlurkAPIError(Exception): pass

class PlurkLoginError(PlurkAPIError): pass
class PlurkNotLoggedIn(PlurkAPIError): pass

class PlurkMissingArgument(PlurkAPIError): pass
class PlurkInvalidArgument(PlurkAPIError): pass