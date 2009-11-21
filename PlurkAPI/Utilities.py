# encoding: utf-8
"""
Utilities.py

Created by Katharine Berry on 2009-11-20.
Copyright (c) 2009 AjaxLife Developments. All rights reserved.
"""

import re
import datetime
from Models import *

VALID_QUALIFIERS = (
    'loves', 
    'likes', 
    'shares', 
    'gives', 
    'hates', 
    'wants', 
    'has', 
    'will', 
    'asks', 
    'wishes', 
    'was', 
    'feels',
    'thinks',
    'says',
    'is',
    ':',
    'freestyle',
    'hopes',
    'needs',
    'wonders'
)

LANGUAGES = {
    'en': 'English',
    'pt_BR': 'Português',
    'cn': '中文 (中国)',
    'ca': 'Català',
    'el': 'Ελληνικά',
    'dk': 'Dansk',
    'de': 'Deutsch',
    'es': 'Español',
    'sv': 'Svenska',
    'nb': 'Norsk bokmål',
    'hi': 'Hindi',
    'ro': 'Română',
    'hr': 'Hrvatski',
    'fr': 'Français',
    'ru': 'Pусский',
    'it': 'Italiano ',
    'ja': '日本語',
    'he': 'עברית',
    'hu': 'Magyar',
    'ne': 'Nederlands',
    'th': 'ไทย',
    'ta_fp': 'Filipino',
    'in': 'Bahasa Indonesia',
    'pl': 'Polski',
    'ar': 'العربية',
    'fi': 'Finnish',
    'tr_ch': '中文 (繁體中文)',
    'tr': 'Türkçe',
    'ga': 'Gaeilge',
    'sk': 'Slovenský',
    'uk': 'українська',
    'fa': 'فارسی',
}

def normalise_offset(offset):
    if isinstance(offset, basestring):
        # Basic validation of the date format
        if not re.match('^[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}T[0-9]{2}:[0-9]{2}:[0-9]{2}$', offset):
            raise ValueError
        return offset
    elif isinstance(offset, datetime.datetime):
        # Convert datetime to UTC and produce the format Plurk likes.
        # There must be a neater way to do this.
        return datetime.datetime(*offset.utctimetuple()[0:6]).isoformat()[0:19]
    elif isinstance(offset, datetime.timedelta):
        # Subtract the delta from the current time and use that.
        return (datetime.datetime.utcnow() - offset).isoformat()[0:19]
    else:
        raise ValueError
        
def normalise_integer_list(ints):
    try:
        return '[%s]' % int(ints)
    except:
        newints = []
        for i in ints:
            newints.append(int(i))
        return '[%s]' % ','.join(newints)

def normalise_plurk_id(plurk_id):
    try:
        return int(plurk_id)
    except:
        pass
    if isinstance(plurk_id, basestring):
        if plurk_id.isalnum():
            plurk_id = int(plurk_id, 36)
        else:
            raise ValueError
    else:
        raise TypeError

def parse_time(time):
    return datetime.datetime.strptime(time, '%a, %d %b %Y %H:%M:%S %Z').date()

def parse_plurk_list(plurks):
    newlist = []
    for plurk in plurks:
        newlist.append(Plurk(plurk))
    return newlist

def parse_user_list(users):
    newlist = []
    for plurk in plurks:
        newlist.append(User(plurk))
    return newlist

        