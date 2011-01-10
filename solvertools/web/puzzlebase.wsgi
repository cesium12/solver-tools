activate_this = '/opt/sages/solvertools/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
from solvertools.web.puzzlebase import app as application
import sys
sys.stdout = sys.stderr
