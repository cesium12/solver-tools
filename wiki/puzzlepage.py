# -*- coding: utf-8 -*-
"""
This module allows Python code to interact with pages on MysteryWiki. It builds
on the "wikitools" Python module, which makes Wiki pages appear as Python
objects.

>>> page = PuzzlePage.get("Horror Metapuzzle 4")
>>> page.getEditGrids()
['HorrorMetapuzzle4']
>>> page.getProperties()['solution']
u'JEANNE DIXON / QUE SERA SERA'
"""

from wikitools import Wiki, Page
from solvertools.config import DB_PASSWORD
import re

site = Wiki('http://manicsages.org/mystery/api.php')
site.login('Solvertools', DB_PASSWORD)

EDITGRID_RE = re.compile(r'<editgrid\s*name="([^"]*)"\s*/?>')
PROPERTY_RE = re.compile(r'\|\s*([^\n=]*)\s*=\s*([^\n]*)\n')

class PuzzlePage(Page):
    """
    An object that lets Python code interact with Wiki pages.

    In addition to the methods defined here, you may also be interested in the
    getWikiText() method, which gets the source text of the page.
    """

    def getEditGrids(self):
        """
        Get a list of EditGrid IDs for all the EditGrids on the page.
        """
        text = self.getWikiText().decode('utf-8')
        gridnames = EDITGRID_RE.findall(text)
        return [editgrid_safe_name(name) for name in gridnames]
    
    def getProperties(self):
        """
        Get a dictionary of semantic properties that are set on the page
        through the Puzzle20?? template. Plus, possibly, some spurious matches.
        """
        props = {}
        text = self.getWikiText().decode('utf-8')
        for key, val in PROPERTY_RE.findall(text):
            props[key] = val
        return props

    def getSolution(self):
        """
        Get the posted solution to the puzzle, or the empty string if it is
        not yet on the page.
        """
        return self.getProperties()['solution']

    @staticmethod
    def get(title):
        """
        Gets a PuzzlePage object for the page with the given title. This does
        not check to see if the page actually exists (you can write a new page
        this way).
        """
        return PuzzlePage(site, title)

def editgrid_safe_name(text):
    u"""
    Transforms an EditGrid name into the "safe" name that is actually used
    to reference the grid.

    >>> editgrid_safe_name(u"Test (in_ñg!)")
    'Testing'
    """
    if isinstance(text, unicode):
        text = text.encode('utf-8')
    return re.sub("[\W_]", "", text)

