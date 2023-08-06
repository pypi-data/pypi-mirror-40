import sys
import numpy as np

GOV_ATTRS = ['gw', 'gl', 'gp', 'gf']

transshow = {'f': 'Function',
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

tok_trans = {'-LCB-': '{',
             '-RCB-': '}',
             '-LRB-': '(',
             '-RRB-': ')',
             '-LSB-': '[',
             '-RSB-': ']'}

APP_STRING = 'Contents/MacOS/lib/python{}/buzzword'.format(sys.version[:3])
