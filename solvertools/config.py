"""
Configuration options for Solvertools.

This tells Solvertools how to log into some external services, like the
database on bach.manicsages.org or the Google account. This requires a
password which is ''not'' included in the code, but which you can get from
the mailing list.

Before you can use these services, you need to make a file called
`secrets.py` in the `solvertools/` package directory, containing one line:

    PASSWORD='passwordgoeshere'

"""

import logging
logger = logging.getLogger(__name__)
try:
    from solvertools.secrets import PASSWORD
except ImportError:
    logger.warn("Couldn't find the password.")
    logger.warn("Please make a file called 'solvertools/secrets.py' "
                "containing this line:\n\nPASSWORD='passwordgoeshere'\n")
    PASSWORD=''

DB_USERNAME='sages'
DB_PASSWORD=PASSWORD
GOOGLE_USERNAME='manicscript'
GOOGLE_PASSWORD=PASSWORD
DB_HOST='bach.manicsages.org'
DB_PORT=5432
DB_NAME='puzzlebase'

#DB_URL='postgresql://%s:%s@%s:%s/%s' % (DB_USERNAME, DB_PASSWORD, DB_HOST,
#                                        DB_PORT, DB_NAME)
from solvertools.util import get_db
DB_URL='sqlite:///'+get_db('puzzlebase.db')
EDITGRID = {
    'USERNAME': 'sages/sages',
    'PASSWORD': PASSWORD,
    'APP_KEY': '5a2e2afe2465a26af2eccb72',
    'WORKSPACE': 'sages/common'
}

