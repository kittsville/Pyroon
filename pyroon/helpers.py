# -*- coding: utf-8 -*-

"""
pyroon.helpers
~~~~~~~~~~~~~~~
Useful little methods to perform various tasks
"""

from unidecode import unidecode

def getRooText(comment):
    """
    Filters non-roo junk like "Edit: Thanks for gold"
    """
    
    return unidecode(comment.partition('\n')[0]).rstrip('.').rstrip('!')
