# -*- coding: utf-8 -*-

"""
pyroon.main
~~~~~~~~~~~~~~~
This module performs recursively explores roos
"""

import praw
import re
import json
import time
from .config import getRedditAuth
from .helpers import getRooText, recoverDeletedComment
from bs4 import BeautifulSoup

COMMENT_ID_RE = re.compile('reddit\.com/r/[0-9a-z_]{3,21}/comments/[0-9a-z]+/.+/([0-9a-z]+)', re.I)

class Pyroon():
    def __init__(self):
        self.version   = '0.1.0'
        self.roos      = {}
        self.roo_links = {}
        self.reddit    = praw.Reddit(**getRedditAuth())
    
    def loadGraph(self, file_name, merge=True):
        """
        Loads roos and their links from JSON file, opposite of saveGraph
        """
        with open(file_name, 'r') as file:
            saved_graph = json.load(file)
        
        if saved_graph['pyroon_version'] != self.version:
            raise ValueError(
                'Tried to use Pyroon v{0} to load graph made by v{1}'.format(
                    self.version,
                    saved_graph['pyroon_version']
                )
            )
        
        if saved_graph['format'] != 'pyroon':
            raise ValueError("Can't load incompatible graph format {0}").format(saved_graph['format'])
        
        if merge:
            self.roos.update(saved_graph['roos'])
            self.roo_links.update(saved_graph['roo_links'])
        else:
            self.roos      = saved_graph['roos']
            self.roo_links = saved_graph['roo_links']
        
        roo_count      = len(saved_graph['roos'])
        roo_link_count = len(saved_graph['roo_links'])
        
        'Loaded {0} roos and {1} links from "file_name"'.format(
            roo_count,
            roo_link_count,
            file_name
        )
    
    def addRoo(self, comment_url, limit=float('inf'), first_roo=False):
        """
        Adds chain of connected roos
        """
        previous_roo = None
        
        roos = 0
        
        while roos < limit:
            roos += 1
            
            comment_id_match = COMMENT_ID_RE.search(comment_url)
            
            if comment_id_match:
                comment_id = comment_id_match.group(1)
            else:
                break
            
            if previous_roo:
                roo_link_id = '{0}>{1}'.format(previous_roo['id'], comment_id)
                
                roo_link = {
                    'id'      : roo_link_id,
                    'source'  : previous_roo['id'],
                    'target'  : comment_id,
                    'url'     : comment_url,
                    'deleted' : comment_deleted,
                }
                
                self.roo_links[roo_link_id] = roo_link
            
            # If comment ID is already stored then job done!
            if comment_id in self.roos:
                break
            
            comment = self.reddit.comment(comment_id)
            
            if (comment.body == '[removed]' or comment.body == '[deleted]') and comment.author is None:
                comment_deleted     = True
                roo_link['deleted'] = True
                
                comment = recoverDeletedComment(comment_id, self.reddit)
                
                if comment is None:
                    break
            else:
                comment_deleted = False
            
            comment_soup = BeautifulSoup(
                comment.body_html,
                'html.parser'
            )
            
            comment_text = comment_soup.get_text()
            
            roo = {
                'id'      : comment_id,
                'text'    : comment_text,
                'sub'     : str(comment.subreddit),
                'url'     : 'https://reddit.com' + comment.permalink(fast=True),
                'deleted' : comment_deleted,
                'first'   : first_roo,
            }
            
            self.roos[comment_id] = roo
            
            if first_roo:
                first_roo = False
            
            hyperlink = comment_soup.select_one('a')
            
            if hyperlink == None:
                roo['name'] = 'Not a roo'
                break
            else:
                roo['name'] = getRooText(comment_text) or 'Ah, the old Reddit switch-a-roo'
                
                print roo['name']
            
            comment_url = hyperlink['href']
            
            previous_roo = roo
    
    def discardOrphanRoos(self):
        """
        Removes all roos with no links to or from other roos
        """
        linked_roos = set()
        
        for roo_link_id in self.roo_links:
            roo_link = self.roo_links[roo_link_id]
            
            linked_roos.add(roo_link['target'])
            linked_roos.add(roo_link['source'])
        
        roo_ids = self.roos.keys()
        
        for roo_id in roo_ids:
            if roo_id not in linked_roos:
                del self.roos[roo_id]
        
    def saveGraph(self, file_name):
        """
        Exports graph of connected roos 
        """
        output = {
            'pyroon_version' : self.version,
            'created'        : int(time.time()),
            'format'         : 'pyroon',
            'roos'           : self.roos,
            'roo_links'      : self.roo_links,
        }
        
        with open(file_name, 'w+') as output_file:
            json.dump(output, output_file)
        
        roo_count      = len(self.roos)
        roo_link_count = len(self.roo_links)
        
        'Saved {0} roos and {1} links to "file_name"'.format(
            roo_count,
            roo_link_count,
            file_name
        )
    def exportCytoscapeGraph(self, file_name):
        """"
        Exports roo graph in format compatible with Cytoscape.js
        """
        graph = []
        
        graph += [{'data': roo} for _, roo in self.roos.iteritems()]
        graph += [{'data': roo_link} for _, roo_link in self.roo_links.iteritems()]
        
        output = {
            'pyroon_version' : self.version,
            'created'        : int(time.time()),
            'format'         : 'cytoscape',
            'graph'          : graph
        }
        
        with open(file_name, 'w+') as output_file:
            json.dump(output, output_file)
