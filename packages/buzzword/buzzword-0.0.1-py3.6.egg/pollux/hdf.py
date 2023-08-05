import os
import pandas as pd
import numpy as np
from polly import Corpus
import json
import gc
from .config import CORPUS_DIR, TOP_RESULTS, COLLAPSE_TREE_PUNCTUATION
from .jsons import make_all_views_for


def store_as_hdf(self, path=False, name=False, colmax={}, **kwargs):
    """
    Create an HDF5-stored corpus from Corpus or LoadedCorpus
    """
    # get name of corpus
    if name is False:
        name = getattr(self, 'name', os.path.basename(self.path))

    # generate a path to the file if need be
    if not path:
        path = os.path.join(self.path, name + '.h')
    else:
        path = os.path.expanduser(path)

    # if the file exists, delete this table from it
    if os.path.isfile(path):
        store = pd.HDFStore(path)
        if name in [i.lstrip('/') for i in store.keys()]:
            del store[name]

    # load corpus ... perhaps not ideal :)
    if isinstance(self, Corpus):
        corpus = self.load(**kwargs)
    else:
        corpus = self

    # remove bad fields
    corpus = corpus.drop(['d'], axis=1, errors='ignore')

    min_itemsize = {}
    corpsize = len(corpus)

    # convert some columns because of problems with categoricals
    for c in corpus.columns:
        if c in ['s', 'i', 'sent_len', '_n', 'number', 'year',
                 'g', 'c', 'postgroup', 'totalposts', 'postnum', 'postid']:
            corpus[c] = pd.to_numeric(corpus[c], errors='coerce')
        else:
            try:
                pd.to_numeric(corpus[c], errors='raise')
            except:
                corpus[c] = corpus[c].astype(object).fillna('')
                mx = corpus[c].str.len().max()
                if np.isnan(mx):
                    continue
                min_itemsize[c] = mx+1
                print('convert ', c, mx)

    if colmax:
        for k, v in colmax.items():
            if k in corpus.columns:
                try:
                    corpus[k] = corpus[k].str.slice(0,v-1)
                    print('cut %s to %d on %s.' % (k, v, name))
                    min_itemsize[k] = v+1
                except:
                    print('colmax %s failed on %s.' % (k, name))

    corpus = corpus.drop(['file', 's', 'i'], axis=1, errors='ignore')
    corpus = corpus.reset_index(drop=False)

    dcs = [i for i in ['file', 's', 'i', 'text'] if i in corpus.columns]
    if not all(i in corpus.columns for i in ['file', 's', 'i', 'w']):
        raise ValueError('Missing columns')
    chunksize = kwargs.get('chunksize', 80000)
    if len(corpus) > chunksize:
        corpus = np.array_split(corpus, (corpsize // chunksize))
    else:
        corpus = [corpus]

    print("MIN ITEMSIZES", min_itemsize)

    t = False
    if len(corpus) > 1:
        from tqdm import tqdm, tqdm_notebook
        try:
            if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
                tqdm = tqdm_notebook
        except:
            pass
        t = tqdm(total=len(corpus),
                 desc='Saving %s' % name,
                 ncols=120,
                 unit='chunk')

    for i, d in enumerate(corpus, start=1):
        store.append(name,
                     pd.DataFrame(d),
                     format='table',
                     data_columns=dcs,
                     chunksize=chunksize,
                     expectedrows=corpsize,
                     min_itemsize=min_itemsize,
                     index=False)
        if t is not False:
            t.update()

    if t is not False:
        t.close()

    print('Stored as {} in {}'.format(name, path))
    store.close()
    return store


def make_all(table=True, do_json=True, colmax={}, **kwargs):

    USER = False
    UPLOAD_FOLDER = os.path.join(CORPUS_DIR, 'uploads')
    storepath = os.path.join(CORPUS_DIR, 'corpora.h5')
    jsonpath = os.path.join(CORPUS_DIR, 'views.json')

    corpus_json = dict()
    dicts = list()

    try:
        os.remove(storepath)
    except OSError:
        pass

    hdf_ok = True

    try:
        store = pd.HDFStore(storepath)
    except ImportError:
        hdf_ok = False
        print("\n\nWARNING: HDF5 not installed. This will slow things down.\n\n")

    projects = [os.path.join(CORPUS_DIR, d) for d in os.listdir(CORPUS_DIR)
                if os.path.isdir(os.path.join(CORPUS_DIR, d)) and d not in ['uploads', '_tmp']]

    # add user projects
    if not os.path.isdir(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if USER is not False:
        user_dirs = [os.path.join(UPLOAD_FOLDER, USER)]
    else:
        user_dirs = [d for d in os.listdir(UPLOAD_FOLDER) if os.path.isdir(os.path.join(UPLOAD_FOLDER, d))]

    for d in user_dirs:
        userdir = os.path.join(UPLOAD_FOLDER, d)
        user_corp = [os.path.join(userdir, d) for d in os.listdir(userdir) if os.path.isdir(os.path.join(userdir, d)) and d.endswith('-parsed')]
        for i in user_corp:
            projects.append(i)

    # turn each project into a dict for the table
    for xx, parsed in enumerate(projects):

        corpus = Corpus(parsed)
        path = corpus.path
        nfiles = len(corpus.files)
        lang = 'en'
        desc = 'No description'
        name = os.path.basename(corpus.path.replace('-parsed', ''))
        print('Starting: %s' % name)
        corpus = corpus.load(load_trees=not table)

        print("Creating store for %s ..." % name)

        kwargs = {'corpus_name': name,
                  'corpus': False,
                  'TOP_RESULTS': TOP_RESULTS,
                  'COLLAPSE_TREE_PUNCTUATION': COLLAPSE_TREE_PUNCTUATION}

        print('COLS:', corpus.columns)

        if do_json:
            corpus_json[name] = make_all_views_for(corpus, is_new=True, corp=corpus, cols=corpus.columns, **kwargs)

            cdict = {'name': name,
                     'path': path,
                     'lang': lang,
                     'desc': desc,
                     'parsed': "True",
                     'nsents': format(0, ','),
                     'nfiles': format(nfiles, ',')}

            dicts.append(cdict)
            print('JSON generated for %s' % name)

        if hdf_ok:
            print('Corpus prepared')
            store_as_hdf(corpus, path=storepath, name=name, colmax=colmax, **kwargs)
            corpus = None
            del corpus
            gc.collect()

    if do_json:
        from corpkit.jsons import JEncoder
        tup = [dicts, corpus_json]
        with open(jsonpath, 'w') as outfile:
            print('Writing JSON ... ')
            json.dump(tup, outfile, cls=JEncoder)
