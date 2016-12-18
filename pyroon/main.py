# -*- coding: utf-8 -*-

"""
pyroon.main
~~~~~~~~~~~~~~~
This module performs recursively explores roos
"""

import praw
import re
from .config import getRedditAuth
from bs4 import BeautifulSoup, SoupStrainer

COMMENT_ID_RE = re.compile('reddit\.com/r/[0-9a-z_]+/comments/[0-9a-z]{6}/[0-9a-z_]+/([0-9a-z]+)', re.I)
LINK_FILTER = SoupStrainer('a')

def pyroon(comment_url):
    reddit = praw.Reddit(**getRedditAuth())
    
    while True:
        comment_id_match = COMMENT_ID_RE.search(comment_url)
        
        if comment_id_match:
            comment_id = comment_id_match.group(1)
        else:
            break
        
        comment = reddit.comment(comment_id)
        
        roo_link = BeautifulSoup(comment.body_html, 'html.parser', parse_only=LINK_FILTER).select_one('a')
        
        if roo_link == None:
            break
        
        print roo_link.text
        comment_url = roo_link['href']