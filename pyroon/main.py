# -*- coding: utf-8 -*-

"""
pyroon.main
~~~~~~~~~~~~~~~
This module performs recursively explores roos
"""

import praw
import re
import json
from .config import getRedditAuth
from bs4 import BeautifulSoup

COMMENT_ID_RE = re.compile('reddit\.com/r/[0-9a-z_]+/comments/[0-9a-z]{6}/[0-9a-z_]+/([0-9a-z]+)', re.I)

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
    
    def addRoo(self, comment_url):
        """
        Adds chain of connected roos
        """
        last_roo = None
        
        while True:
            comment_id_match = COMMENT_ID_RE.search(comment_url)
            
            if comment_id_match:
                comment_id = comment_id_match.group(1)
            else:
                break
            
            # If comment ID is already stored then job done!
            if comment_id in self.roos:
                break
            
            comment = self.reddit.comment(comment_id)
            
            comment_soup = BeautifulSoup(
                comment.body_html,
                'html.parser'
            )
            
            roo = {
                'id'   : comment_id,
                'text' : comment_soup.get_text(),
            }
            
            self.roos[comment_id] = roo
            
            roo_link = comment_soup.select_one('a')
            
            if last_roo:
                roo_link_id = '{0}>{1}'.format(last_roo['id'], roo['id'])
                
                self.roo_links[roo_link_id] = {
                    'id'     : roo_link_id,
                    'source' : last_roo['id'],
                    'target' : roo['id'],
                }
            
            if roo_link == None:
                roo['name'] = 'Not a roo'
                break
            else:
                roo['name'] = roo_link.get_text()
            
            print roo['name']
            
            comment_url = roo_link['href']
            
            last_roo = roo
        
    def saveGraph(self, file_name):
        """
        Exports graph of connected roos 
        """
        output = {
            'pyroon_version' : self.version,
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
            'format'         : 'cytoscape',
            'graph'          : graph
        }
        
        with open(file_name, 'w+') as output_file:
            json.dump(output, output_file)
