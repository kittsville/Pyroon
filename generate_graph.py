# -*- coding: utf-8 -*-

"""
generate_graph
~~~~~~~~~~~~~~~
Generates graph in /docs
"""

from pyroon import Pyroon
import os

LOCAL_DIR = os.path.dirname(__file__)
SAVE_PATH = os.path.join(LOCAL_DIR, 'docs/graph.json')

pyroon = Pyroon()

pyroon.addRoo('https://www.reddit.com/r/woahdude/comments/5juiaf/well_of_death/dbjddli/')
pyroon.exportCytoscapeGraph(SAVE_PATH)

pyroon.saveRoo('save.json') # Stored roo graph in form Pyroon can load and merge with other graphs
