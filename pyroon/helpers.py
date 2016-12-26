# -*- coding: utf-8 -*-

"""
pyroon.helpers
~~~~~~~~~~~~~~~
Useful little methods to perform various tasks
"""

from unidecode import unidecode
import praw
import requests

def getRooText(comment):
    """
    Filters non-roo junk like "Edit: Thanks for gold"
    """
    
    majorly_filtered = unidecode(comment.partition('\n')[0])
    
    minorly_filtered = majorly_filtered.split('(', 1)[0].rstrip().rstrip('.').rstrip('!')
    
    return minorly_filtered

def recoverDeletedComment(comment_id, reddit):
    """
    Attempts to recover deleted roo using PushShift Reddit API
    """
    api_query_base = 'https://api.pushshift.io/reddit/search?ids='
    
    query_url = api_query_base + comment_id
    
    response = requests.get(query_url, timeout=10)
    
    if response.status_code != 200:
        print 'not 200'
        return None
    
    query_results = response.json()
    
    if query_results['metadata']['results'] == 1:
        comment_data = query_results['data'][0]
        
        # Creates PRAW comment instance from PushShift API data
        return praw.models.Comment(reddit, _data=comment_data)
    else:
        return None
