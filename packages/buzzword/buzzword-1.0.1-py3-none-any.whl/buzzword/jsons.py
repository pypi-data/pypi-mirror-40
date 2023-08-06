"""
Utilities for creating JSON, used in buzzword to display in tables, charts, etc.
"""
import os
import pandas as pd
import numpy as np
import json
from .constants import transshow
from .config import MAX_CONC_ROWS, TOP_RESULTS


class JEncoder(json.JSONEncoder):
    """
    Custom JSON encoder that handles numpy objects
    """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super().default(obj)


def remove_path(filepath):
    return os.path.splitext(filepath.split('-parsed/', 1)[-1])[0]


def add_fsi_to_cols(df, remove_paths=True):
    df = df.drop(['file', 's', 'i'], axis=1, errors='ignore')
    df = df.reset_index(drop=False)
    df['file'] = df['file'].apply(remove_path)
    return df


def sentence_table(df):
    """
    Turn LoadedCorpus into sentence table
    """
    # get just the root
    df = df[df['g'] == 0]
    # call text sentence
    df['sentence'] = df['text'].astype(str)
    rename = ['w', 'l', 'x', 'p']
    head_names = list()
    for bit in rename:
        name = 'head {}'.format(transshow[bit]).lower()
        head_names.append(name)
        df[name] = df[bit]

    df = add_fsi_to_cols(df, remove_paths=True)
    df = df.drop(['text', 'g'], axis=1, errors='ignore')
    order = ['s', 'sentence', 'file', 'subcorpus', 'head'] + head_names
    order = [i for i in order if i in df.columns]
    df = df.set_index('s')
    df = df[order[1:]]  # i.e. no s
    return df


def truncate(line, fromleft=False, size=80):
    """
    Truncate a string from left or right to size in characters
    """
    if not line or isinstance(line, float):
        return ''
    if not fromleft:
        return line if len(line) < size-1 else line[:size-3] + '...'
    else:
        return line if len(line) < size-1 else '...' + line[-size+3:]


def table_json(res, is_new=False, kind='conc', fmt_kwargs={}, corp=False, **kwargs):
    """
    Generate JSON data for the table or concordance

    Args:
        res (Results): data to make a table from

    Return:
        data, cols: the needed json
    """
    from buzzword.config import DECIMALS

    link_num = 1 if is_new else 2

    if kind == 'conc':
        l_or_r = 'left'
        if is_new:
            cnc = sentence_table(res)
        else:
            cnc = res[:MAX_CONC_ROWS].conc(no_punct=False, df=corp, **fmt_kwargs)
            cnc = cnc.drop('text', axis=1, errors='ignore')

        res = pd.DataFrame(cnc)
        badcol = [i for i in list(res.columns) if i.startswith('_') or i in ['parser', 'sent_id']]
        res = res.drop(badcol, axis=1, errors='ignore')

        aligns = {'left':     'right',
                  'match':    'center',
                  'sentence': 'left',
                  '#':        'right',
                  's':        'right',
                  'i':        'right'}

        widths = {'left':        '40%',
                  'match':       '15%',
                  'right':       '40%',
                  'sentence':    '80%'}

        if not fmt_kwargs.get('colour'):
            if not is_new:
                res['left'] = res['left'].apply(truncate, fromleft=True, size=120)
                res['match'] = res['match'].apply(truncate, fromleft=False, size=50)
                res['right'] = res['right'].apply(truncate, fromleft=False, size=120)
            else:
                res['sentence'] = res['sentence'].apply(truncate, fromleft=False, size=340)
        try:
            res = res.reset_index()
        except ValueError:
            res.index.names = [i + ' ' for i in res.index.names]
            res = res.reset_index()

    else:
        l_or_r = 'right'
        aligns = dict()
        widths = dict()
        subc = fmt_kwargs.pop('subcorpora', 'default')
        res = res.table(subcorpora=subc, df=corp, is_new=is_new, **fmt_kwargs)
        res = res.ix[0:9999, 0:9999]
        if fmt_kwargs.get('relative', False) is not False:
            res = res.round(decimals=DECIMALS)
        names = [str(i) for i in res.index.names]
        res.index.names = names
        try:
            res = res.reset_index()
        except ValueError:
            res.index.names = [i + ' ' for i in res.index.names]
            res = res.reset_index()

    col_list = list(res.columns)

    check_col = {'field': '_state',
                 'id': 'delete_' + kind + '_title',
                 'title': 'Delete',
                 'checkbox': 'true',
                 'align': 'center',
                 'valign': 'middle'}

    cols = [{'id': k,
             'title': k,
             'field': k,
             'halign': aligns.get(k, l_or_r),
             'align': aligns.get(k, l_or_r),
             'sortable': "true"} for k in col_list]

    if kind == 'conc':
        cols[link_num]['formatter'] = 'fsiFormatter'
        for c in cols:
            c['width'] = widths.get(c['field'], '30px')
        if not is_new:
            cols[link_num-1]['sorter'] = 'leftSorter'

    else:
        for i in range(len(names)):
            cols[i].update({'formatter': 'ixFormatter',
                            'halign': 'left',
                            'align': 'left'})

    cols = [check_col] + cols
    data = list(res.T.astype(str).to_dict().values())

    return dict(data=data, columns=cols)


def pivot_json(res, is_new=False, corp=False):
    """
    Make the pivot table
    """
    # for entire corpora, the corpus is the dataset. for searches,
    # we get the matching rows of the corpus
    res = res if is_new else corp.loc[res.index]
    res = add_fsi_to_cols(res, remove_paths=True)
    # one exception is when the user searches by metadata. here, is_new is True
    # because we want to show sentences, not words
    if not len(res.columns):
        res = corp.iloc[res.index]
    # the problem here is that this gets the n most common words, then
    # gets all instances of them. so, in 10 million word corpora, this could
    # easily be 1m rows or so!
    res = res.head(10000)
    ws = res['w'].str.lower().value_counts().head(TOP_RESULTS)
    res = res[res['w'].isin(ws.index)]
    res = pd.DataFrame(res.drop(['parse', 'text'], axis=1, errors='ignore'))
    res = fix_columns(res)
    # res.index = res.index + 1
    return list(res.T.astype(str).to_dict().values())


def tree_json(res, move=False, is_new=False, corp=False, current_ix=None):
    """
    Load or build the json needed for a displacy tree

    Return:
        Response/json
    """
    # if we're browing an unsearched corpus, we just get each sentence in the corpus
    if is_new:
        res = corp[corp.index.get_level_values('i') == 1]
    # Otherwise, we have an Interrogation, so we get each match
    else:
        res = corp.loc[res.index]

    res = res.reset_index()

    res_index = list(res.index)
    if not current_ix:
        current_ix = res_index[0]

    # navigating from the toolbar in the tree view
    if move in ['start', 'end', 'minus', 'plus']:
        if move == 'start':
            thix = 0
        elif move == 'end':
            thix = res_index[-1]
        elif move == 'minus':
            thix = current_ix - 1
        elif move == 'plus':
            thix = current_ix + 1

    elif not move:
        thix = res_index[0]

    # don't know what's going on here
    try:
        row = res.loc[thix]
    except:
        row = res.iloc[thix]

    sent = corp.set_index(['file', 's', 'i']).loc[(row.file, row.s)]

    # generate list of matches (?)
    matches = False
    if not is_new:
        matches = list()
        t_matches = [row.i]
        for t in t_matches:
            if isinstance(t, str) and '-' in t:
                raise NotImplementedError
            else:
                matches.append(int(t))

    sent_json = make_input_for_tundra_vis(sent, matches)
    cons_json = sent_to_constituency_json(sent, matches)

    return sent_json, cons_json, thix


def make_input_for_tundra_vis(sent, matches, **kwargs):
    """
    Generate the JSON needed for tundra visualisation of dependency graph
    """
    links = list()
    nodes = list()
    if not all(x in sent.columns for x in ['w', 'f', 'g']):
        return None

    COLLAPSE_TREE_PUNCTUATION = kwargs.get('COLLAPSE_TREE_PUNCTUATION', True)
    if COLLAPSE_TREE_PUNCTUATION:
        sent = affix_punct(sent)

    tokens = list(sent['w'])
    text = ' '.join(tokens)
    sent = sent.copy()
    sent['_rangeix'] = list(range(len(sent)))

    # make attrib for every token
    # i is the real zero index, whereas start is the token id
    for i, (start, row) in enumerate(sent.iterrows()):
        if isinstance(start, tuple):
            start = start[-1]

        categories = {'lemma': row.get('l', '_'),
                      'pos': row.get('p'),
                      'text': row.get('w'),
                      'head': str(row.get('g', '_'))}

        node = {'name': row['w'],
                'node': 'n%d' % i,
                'ix': int(start),
                'categories': categories}

        nodes.append(node)

        if row['f'] == 'punct':
            continue
        # the governor might have been removed ... skip if need be
        if int(row['g']) > 0 and int(row['g']) not in list(sent.index):
            continue

        # get the zero indexed position of the governor
        ix = row['g'] - 1

        if ix == -1:
            idx = 'nr_n%d' % i
            ix = i
        else:
            # get the zero index for the governor
            ix = sent.loc[row['g']]['_rangeix']
            idx = 'n%d_n%d' % (ix, i)

        link = {'id': idx,
                'dependency': row['f'],
                'source': int(ix),
                'target': int(i)}

        if row['g'] == 0:
            link['root'] = True

        links.append(link)

    d3dict = {'isfake': False,
              'links': links,
              'nodes': nodes,
              'tokens': tokens,
              'text': text,
              'matches': matches if matches else False}

    #sent.drop('_rangeix', axis=1, errors='ignore', inplace=True)
    return d3dict


def affix_punct(sent):
    """
    Heuristically move punctuation tokens onto the previous/next token,
    then remove the token from the sentence, to improve the look of dep graphs
    """
    if 'f' not in sent.columns:
        return sent

    from corpkit.constants import tok_trans

    words = list(sent['w'])
    for index, (i, row) in enumerate(sent.copy().iterrows()):
        if row['f'] == 'punct' or row['w'] in tok_trans:
            tok = tok_trans.get(row['w'], row['w'])
            if not index:
                words[index+1] = tok + words[index+1]
            else:
                words[index-1] += tok

    sent = sent.copy()
    sent['w'] = words
    sent = sent[sent['f'] != 'punct']
    return sent


def make_all_views_for(res, is_new, fmt_kwargs={}, corp=False, current_ix=None):
    """
    Generate all the views for a search or edit result
    """
    # we show a pos distribution for new corpora table view to save memory
    if is_new:
        tab_fmt_kwargs = dict(show=['p'], subcorpora='default')
        conc_fmt_kwargs = dict(show=['w'])
    else:
        tab_fmt_kwargs = fmt_kwargs
        conc_fmt_kwargs = fmt_kwargs

    # this tells the frontend which views need updating
    need_update = ['conc', 'pivot', 'table']
    conc = table_json(res, is_new=is_new, kind='conc', fmt_kwargs=conc_fmt_kwargs, corp=corp)
    table = table_json(res, is_new=is_new, kind='table', fmt_kwargs=tab_fmt_kwargs, corp=corp)
    #tree, cons, fsi = tree_json(res=res, is_new=is_new, corp=corp, current_ix=current_ix)
    #if tree:
    #    need_update.append('tree')
    #if cons:
    #    need_update.append('cons')

    #print("Making pivot")
    pivot = pivot_json(res, is_new=is_new, corp=corp)

    return dict(table=table,
                conc=conc,
                pivot=pivot,
                #tree=tree,
                #cons=cons,
                sent=None,
                #fsi=fsi,
                needupdate=need_update)


def fix_columns(df):
    """
    Turn l to Lemma etc. for display
    """
    from .constants import transshow
    transshow.update(dict(g='Governor',
                          d='Dependent',
                          s='Sentence',
                          m='Morphology',
                          i='Index'))
    cols = [transshow.get(c, c).lower() for c in list(df.columns)]
    df.columns = cols
    return df


def sent_to_constituency_json(sent, matches):
    """
    Take a sentence as DF and make into json needed for constituency tree view
    """
    first = sent.iloc[0]
    parsetree = first.get('parse')
    if not parsetree:
        return None
    if isinstance(parsetree, str):
        from nltk.tree import ParentedTree
        parsetree = ParentedTree.fromstring(parsetree)

    tree = dict()
    table = list()
    tokens = parsetree.leaves()
    sstring = first['text'] if 'text' in sent.columns else ' '.join(tokens)

    for i, row in sent.iterrows():
        cats = dict(text=row['w'], pos=row['p'], lemma=row['l'], edge='eh')
        # morphology?
        tokinfo = dict(token=row['w'], categories=cats)
        table.append(tokinfo)

    leaf_pos = parsetree.treepositions(order='leaves')
    leaf_pos = [i[:-1] for i in leaf_pos]

    for i, pos in enumerate(parsetree.treepositions(), start=1):
        if i == 1:
            is_root = True
        else:
            is_root = False
        subt = parsetree[pos]
        terminal = isinstance(subt, str)
        idx = 'node_%d' % i
        typ = 'terminal' if terminal else 'main'

        # get every leaf this subtree has
        leaves = False if terminal else list(subt.subtrees(lambda t: t.height() == 2))
        # for the root of the tree

        if leaves:
            start = leaf_pos.index(leaves[0].treeposition()) + 1
            finish = leaf_pos.index(leaves[-1].treeposition()) + 1
            nodes = list()
            order = False
        else:
            start = leaf_pos.index(pos[:-1]) + 1
            finish = start
            nodes = False
            order = leaf_pos.index(pos[:-1]) + 1

        name = subt.label() if not terminal else subt

        posdict = dict(id=idx,               # not sure if needed
                       name=name,     # the label
                       num=str(i),            # a unique digit
                       labels=[],
                       start=str(start),     # 1ix of leftmost token
                       finish=str(finish),   # 1ix of rightmost token
                       type=typ)

        if nodes is not False:
            posdict['nodes'] = list()

        if order is not False:
            posdict['order'] = order
            posdict['categories'] = table[order-1]['categories']

        if is_root:
            tree = posdict

        else:
            temp_tree = tree
            for x in pos[:-1]:
                temp_tree = temp_tree['nodes'][x]
            posdict['parent'] = temp_tree['id']
            posdict['realParent'] = temp_tree['id']
            if terminal:
                posdict['categories']['edge'] = temp_tree['name']
            temp_tree['nodes'].append(posdict)

    return dict(queryMatch=[],
                sentence=sstring,
                tokens=tokens,
                tree=[tree],
                table=table)
