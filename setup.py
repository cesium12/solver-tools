from setuptools import find_packages, setup
from distutils.extension import Extension
import os

def prompt_for_password():
    if not os.access('solvertools/secrets.py', os.F_OK):
        print "You don't have a secrets.py yet."
        print "This script will create one -- you just need to enter the"
        print "low-security Manic Sages password. (It was sent to the"
        print "manic-sages-research list, or you can ask rspeer@mit.edu.)"
        print
        print "If you type the wrong password or leave it blank, only the"
        print "Internet-enabled parts of solvertools won't work."
        print
        print "Password:",
        password = raw_input()
        secrets = open('solvertools/secrets.py', 'w')
        print >> secrets, "PASSWORD=%r" % password
        secrets.close()
        print "Password stored."

def prefix_path(prefix, paths):
    return [os.path.join(prefix, path) for path in paths.split()]

setup(name='solvertools',
      version='2011.0',
      description='Manic Sages Solver Tools',
      packages=find_packages(),
      package_data={
        # Unfortunately, you have to update this if you add a new kind of data
        '': ['data/dict/*.txt', 'data/pickle/*.pickle',
             'data/pickle/*.regulus',
             'data/db/*.npy',
             'data/corpora/answers/*.dat',
             'data/test/*', 'data/codes/*.txt']
      },
      ext_modules=[Extension("solvertools.extensions.regulus._regulus",
          prefix_path('solvertools/extensions/regulus',"regulus.i amtrie.cpp automaton.cpp check.cpp dict.cpp dyntrie.cpp"), swig_opts=['-c++', '-Wall', '-outdir', 'solvertools/extensions/regulus'])],
      install_requires=['ply', 'pymongo', 'wikitools'],
      zip_safe=False,   # dear Setuptools, please don't fuck with my files
     )
prompt_for_password()
