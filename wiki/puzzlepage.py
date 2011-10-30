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
>>> page.getCategories()
[u'Category:Puzzles']
"""

from wikitools import Wiki, Page
from solvertools.config import DB_PASSWORD
import re
import time

site = Wiki('http://manicsages.org/mystery/api.php')
site.login('Solvertools', DB_PASSWORD)

EDITGRID_RE = re.compile(r'<editgrid\s*name="([^"]*)"\s*/?>')
ETHERPAD_RE = re.compile(r'<etherpad\s*name="([^"]*)"\s*/?>')
PROPERTY_RE = re.compile(r'\|\s*([^\n=]*)\s*=\s*([^\n]*)\n')

PUZZLE_PAGE_INIT = u"""{{Puzzle2011
%(props)s
}}

== Solution summary ==
<small>When you solve the puzzle, please briefly describe how you did it here. Off-site solvers and metapuzzlers will thank you.</small>

== Current progress ==
<small>
When you start working on this puzzle, tell the chat box above who and where you are. Even if nobody is here right now, people who come to the page later will see it. When you make significant progress, edit this section and describe it!
</small>

<etherpad name="%(title)s"/>

<!-- Page created by Solvertools -->
"""

GROUP_PAGE_INIT = u"""{{Group2011
%(props)s
}}
"""

def wiki_boolean(value):
    if value and unicode(value).lower()[0:1] in 'ty':
        return u'Yes'
    else:
        return u'No'

def current_timestamp():
    return time.strftime('%Y/%m/%d %I:%M:%S %p')

class PuzzlePage(Page):
    """
    An object that lets Python code interact with Wiki pages.

    In addition to the methods defined here, you may also be interested in the
    getWikiText() method, which gets the source text of the page.
    """

    # Change this manually to False if you want to be able to completely
    # overwrite pages that are in the way.
    safe_mode = True

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

    def getProperty(self, prop):
        """
        Get the value of a given puzzle property on this page, as a Unicode
        string.

        Returns None if that property is unset.
        """
        return self.getProperties().get(prop)

    def setProperty(self, prop, value):
        """
        Change a property on the page (or add it if it is not there), causing
        an edit to the page.

        This should only change the puzzle template, not anything outside it.
        """
        text = self.getWikiText(force=True).decode('utf-8')
        props = self.getProperties()
        prop_re = re.compile(r'\|\s*'+prop+r'\s*=\s*([^\n]*)\n')
        if u"{{Puzzle" not in text:
            raise ValueError("I can't parse this page's puzzle template. "
                             "It may not be a puzzle.")
        if prop in props:
            if props[prop] == value:
                return
            newtext = prop_re.sub(u'|%s=%s\n' % (prop, value), text)
            summary = "solvertools.wiki: setting %s=%s" % (prop, value)
            assert newtext != text
        else:
            newtext = text.sub('}}', '|%s=%s\n}}' % (prop, value), 1)
            assert newtext != text

        result = self.edit(text=newtext,
                           bot=True,
                           summary=summary)
        if result['edit']['result'] != 'Success':
            raise IOError(result)
        return result

    def appendSection(self, title, text):
        """
        Add text to this page in a new section with the given `title`.
        """
        self.edit(appendtext=text,
                  summary=title,
                  bot=True)

    @staticmethod
    def get(title):
        """
        Gets a PuzzlePage object for the page with the given title. This does
        not check to see if the page actually exists (you can write a new page
        this way).
        """
        return PuzzlePage(site, title)

    def initialize_as_puzzle(self, **props):
        if 'group' not in props:
            raise ValueError("You need to specify a group for the puzzle.")
        props['meta'] = wiki_boolean(props.get('meta'))
        props['practice'] = wiki_boolean(props.get('practice'))
        if 'released' not in props:
            props['released'] = current_timestamp()
        proplist = ['|%s=%s' % (k,v) for k,v in props.items()]
        text = PUZZLE_PAGE_INIT % {
            'title': self.title,
            'props': '\n'.join(proplist)
        }
        summary = u'Creating puzzle in group [[%s]] using Solvertools' % props['group']
        if PuzzlePage.safe_mode:
            result = self.edit(text=text.encode('utf-8'),
                               summary=summary.encode('utf-8'),
                               createonly=PuzzlePage.safe_mode)
        else:
            result = self.edit(text=text.encode('utf-8'),
                               summary=summary.encode('utf-8'))
            
        if result['edit']['result'] != 'Success':
            raise IOError(result)
        return result

    def initialize_as_group(self, **props):
        props['practice'] = wiki_boolean(props.get('practice'))
        props['completed'] = wiki_boolean(props.get('completed'))
        if 'released' not in props:
            props['released'] = current_timestamp()
        if 'name' not in props:
            props['name'] = self.title
        proplist = [u'|%s=%s' % (k,v) for k,v in props.items()]
        text = GROUP_PAGE_INIT % {
            'props': u'\n'.join(proplist)
        }
        if PuzzlePage.safe_mode:
            result = self.edit(text=text.encode('utf-8'),
                               summary=u"Creating group using Solvertools",
                               createonly=True)
        else:
            result = self.edit(text=text.encode('utf-8'),
                               summary=u"Creating group using Solvertools")

        if result['edit']['result'] != 'Success':
            raise IOError(result)
        return result

    def page_type(self):
        pass
        
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

def make_puzzle(title, **props):
    u"""
    A high-level function to create a puzzle page on the Wiki.

    Required arguments:

    - title: The title of the puzzle page.
    - group: The name of the group that the puzzle should be in.

    Optional arguments are the same arguments that are used to define a puzzle
    on the Wiki -- that is, 'order', 'url', 'moregroups', 'othername', 'meta',
    'practice', 'importance', 'released', and a few more obscure ones.
    See the Wiki page [[Template:Puzzle2011]] for more information.

    This will refuse to overwrite an existing page, unless you set
    `PuzzlePage.safe_mode = False`.

    Remember to give the argument `practice=True` if it isn't actually a
    Mystery Hunt puzzle.
    """
    page = PuzzlePage.get(title)
    page.initialize_as_puzzle(**props)

def make_group(group_title, puzzle_titles, url=None, name=None, practice=False, parent=None):
    u"""
    A high-level function to create a group full of puzzles simultaneously.

    Required arguments:
    
    - group_title: The (short) title of the group.
    - puzzle_titles: The titles of the puzzles, in order.

    Optional arguments:

    - url: The URL for this puzzle group.
    - name: A longer name for the group.
    - practice: Is this a group of practice puzzles?
    - parent: The name of the parent group.

    The puzzles will be given "order" numbers from 1 to n, in the order you
    gave them in the list. The URLs will all be the same, and no puzzle will be
    marked as a metapuzzle. You can fix these things later.

    This will refuse to overwrite an existing page, unless you set
    `PuzzlePage.safe_mode = False`.
    """
    props = {'practice': practice}
    if parent:
        props['parent'] = parent
    if name is not None:
        props['name'] = name
    if url is not None:
        props['url'] = url
    else:
        props['url'] = ''
    page = PuzzlePage.get(group_title)
    result = page.initialize_as_group(**props)

    for i, puzzle_title in enumerate(puzzle_titles):
        order = i+1
        make_puzzle(puzzle_title, group=group_title, order=order, practice=practice, url=props['url'])
    return result
