from __future__ import with_statement

from os import path
from ConfigParser import SafeConfigParser, NoOptionError
from UserDict import DictMixin

pref_file = path.expanduser("~/.sages.prefs.ini")
default_pref_file = "prefs/sages.defaultprefs.ini"

class Pref(DictMixin):
    def __init__(self, section="General"):
        self.section = section

        self.data = SafeConfigParser()
        read_files = self.data.read( [ default_pref_file, pref_file ] )
        
        if not self.data.has_section(self.section):
            self.data.add_section(self.section)
        

    def __getitem__(self, key):
        # SafeConfigParser uses the wrong type of exception for a missing key in a dictionary.
        # Re-map the exception if necessary.
        try:
            return self.data.get(self.section, key)
        except NoOptionError, e:
            raise KeyError(e)

    def __setitem__(self, key, value):
        self.data.set(self.section, key, value)
        self._save()
        
    def __delitem__(self, key):
        retVal = self.data.remove_option(self.section, key)
        self._save()
        return retVal
        
    def keys(self):
        return [ x[0] for x in self.data.items(self.section) ]


    def _save(self):
        with open(pref_file, "wb") as f:
            self.data.write(f)
        



