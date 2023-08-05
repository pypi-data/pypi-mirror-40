import os
from buzz import Corpus
import json
from .config import CORPUS_DIR, TOP_RESULTS, COLLAPSE_TREE_PUNCTUATION
from .jsons import make_all_views_for, JEncoder


def make_all(table=True, do_json=True, colmax={}, **kwargs):

    USER = False
    UPLOAD_FOLDER = os.path.join(CORPUS_DIR, 'uploads')
    jsonpath = os.path.join(CORPUS_DIR, 'views.json')

    corpus_json = dict()
    dicts = list()

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
        metadata = corpus.metadata
        path = corpus.path
        nfiles = len(corpus.files)
        lang = 'unknown'
        if corpus.name.startswith('UD_'):
            lang = corpus.name.split('_', 1)[1].replace('-parsed', '')
        desc = 'No description'
        name = os.path.basename(corpus.path.replace('-parsed', ''))
        print('Starting: %s' % name)
        loaded = corpus.load(load_trees=not table)

        kwargs = {'corpus_name': name,
                  'corpus': False,
                  'TOP_RESULTS': TOP_RESULTS,
                  'COLLAPSE_TREE_PUNCTUATION': COLLAPSE_TREE_PUNCTUATION}

        if do_json:
            needed = {'table', 'conc', 'pivot', 'sent', 'name', 'path',
                      'lang', 'desc', 'parsed', 'nsents', 'nfiles'}
            if not all(i in metadata for i in needed):
                view_data = make_all_views_for(loaded, is_new=True, corp=loaded, cols=loaded.columns, **kwargs)
                metadata = {'name': name,
                            'path': path,
                            'language': lang,
                            'cons_parser': 'none',
                            'desc': desc,
                            'parser': 'manual',
                            'parsed': 'True',
                            'nsents': format(0, ','),
                            'nfiles': format(nfiles, ','),
                            **view_data}
                corpus.add_metadata(metadata)

            dicts.append(metadata)
            print('JSON generated for %s' % name)

    if do_json:
        tup = [dicts, corpus_json]
        with open(jsonpath, 'w') as outfile:
            print('Writing JSON ... ')
            json.dump(tup, outfile, cls=JEncoder)
