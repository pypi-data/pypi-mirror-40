import os
import numpy as np

CORPUS_DIR = os.path.expanduser('~/corpora')
UPLOAD_DIR = os.path.join(CORPUS_DIR, 'uploads')

# number of different words to show in pivot table
TOP_RESULTS = 50
# not respected yet.
MAX_TABLE_COLUMNS = 9999
MAX_TABLE_ROWS = 9999
MAX_CONC_COLUMNS = 9999
MAX_CONC_ROWS = 9999
# not working yet
THREADS = 3
# port to run app on if not specified manually
PORT = 5555
# number of decimal places to show in tables
DECIMALS = 3
# attempt to not make separate token for comma et al
COLLAPSE_TREE_PUNCTUATION = True
# USE MACOS NOTIFICATION CENTRE
USE_NOTIFICATIONS = True
# minimum time a search must take to attempt OS notification
NOTIFY_MIN_TIME = 10
# MAKE A NOISE WHEN NOTIFICATION OCCURS
NOTIFY_SOUND = False
# MEMORY OPTION ['hdf', 'buzz', 'disk', 'onclick']
MEMORY = 'onclick'

# pre-load some tree json for quicker rendering
PREPARE_FIRST_N_TREES = 10


class CurrentState(object):
    """
    Keep track of things like currently selected corpus
    """
    corpus = False           # the current LoadedCorpus object
    corpus_name = False      # The shortened name of a parsed corpus
    unique_ids = 0           # how many searches done. corpus =0
    just_update = False      # the user wants to refresh display
    subcorpora = ['file']    # default index of table view
    updated_display = False  # the user wants to edit conc or table
    sort_by = False,         # if the user wanted table sorted
    relative = False,        # if the user requested rel/keyness
    corpora_info = dict()    # data for the mainpage display
    show = ['w']             # default way to format tokens in table
    current_ix = False       # index of current tree
    current_conc = None      # columns needed for conc in order to annotate


def get_secret_key():
    """
    Flask wants a unique ID for its session. This grabs a stable key,
    or, if not found, generates one.
    """
    f = os.path.expanduser('~/.flask.key')
    if os.path.isfile(f):
        with open(f, 'r') as fo:
            return fo.read().strip()
    else:
        return os.urandom(24)

# url for sample corpus file 1 and 2
UD_TRAIN = "https://raw.githubusercontent.com/UniversalDependencies/UD_English-EWT/master/en_ewt-ud-train.conllu"
UD_DEV = "https://raw.githubusercontent.com/UniversalDependencies/UD_English-EWT/master/en_ewt-ud-dev.conllu"
# where this corpus should go
UD_DIR = os.path.join(CORPUS_DIR, 'UD_English-parsed')

GOV_ATTRS = ['gw', 'gl', 'gp', 'gf']

SHORT_TO_LONG_SHOW = {'f': 'Function',
                      'l': 'Lemma',
                      'a': 'Distance from root',
                      'w': 'Word',
                      't': 'Trees',
                      'i': 'Index',
                      'n': 'NER',
                      'p': 'POS',
                      'c': 'Count',
                      '+': 'Next',
                      '-': 'Previous',
                      'x': 'XPOS',
                      's': 'Sentence index'}

DTYPES = {'i': np.int32,
          's': np.int64,
          'w': 'category',
          'l': 'category',
          'p': 'category',
          'x': 'category',
          'g': np.int64,
          'parse': object,
          'f': 'category',
          'm': str,
          'o': str,
          'n': 'category',
          'gender': 'category',
          'speaker': 'category',
          'year': np.int64,  # 'datetime64',
          'date': 'category',  # 'datetime64',
          'month': 'category',  # 'datetime64',
          'postgroup': np.float64,
          'totalposts': np.float64,
          'postnum': np.float64}

CONLL_COLUMNS_V2 = ['i', 'w', 'l', 'x', 'p', 'm', 'g', 'f', 'e', 'o']
