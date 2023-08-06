#!/usr/bin/env python

import json
import os
import shutil
import socket
import sys
import threading
import time
import webbrowser

from collections import OrderedDict, defaultdict

from buzz import Corpus

from flask import Flask, \
                  render_template, \
                  redirect, \
                  url_for, \
                  request, \
                  jsonify, \
                  flash

from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import TextField, \
                    RadioField, \
                    BooleanField, \
                    SubmitField

from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename

import buzzword

# config stores potentially configurable settings, which
# in future could be a json file ~/.buzzword.json
from .config import CORPUS_DIR, \
                    UPLOAD_DIR, \
                    get_secret_key, \
                    MAX_CONC_ROWS, \
                    USE_NOTIFICATIONS, \
                    NOTIFY_SOUND, \
                    NOTIFY_MIN_TIME, \
                    PORT, \
                    GOV_ATTRS, \
                    SHORT_TO_LONG_SHOW, \
                    DTYPES, \
                    CONLL_COLUMNS_V2, \
                    CurrentState

from .jsons import table_json, tree_json, make_all_views_for, JEncoder

from .utils import get_corpora_dict, \
                   get_template_dir, \
                   cmd_line_to_kwargs, \
                   notifier, \
                   can_use_rumps

# copy over basic corpus data if not there
# if the data is not available, get it online
CORPORA = os.path.join(os.path.dirname(buzzword.__file__), 'corpora')

# corpora json data is the 'default view' for each available corpus
# it should be generated once for each corpus, to save time
with open(os.path.join(CORPUS_DIR, 'views.json'), 'r') as fo:
    CORPORA_JSON = json.load(fo)

ANNOTATIONS = defaultdict(list)

# files the user can upload
ALLOWED_EXTENSIONS = {'txt', 'xml', 'srt', 'conll', 'conllu', 'tcf', 'xml'}

# names for each template, done like this in case we need to
# modify their paths, though it seems we don't need to because
# flask has kwargs: template_folder and static_folder
TEMPLATES = dict(parse_pop='parse-popup.html',
                 annotate_pop='annotate-modal.html',
                 index='index.html',
                 about='about.html',
                 viewer='viewer.html',
                 select_relative='select-relative.html',
                 tree_modal='tree-modal.html',
                 chart_modal='chart-modal.html',
                 query_history='query-history.html',
                 query_form='query-form.html',
                 explore='explore.html',
                 preferences='preferences.html')

# path to app icon
iconpath = os.path.join(os.path.dirname(buzzword.__file__), 'static', 'favicon.icns')

# check if notifications are even possible
try:
    import rumps
    rumps.debug_mode(True)
    import objc
    nsd = objc.lookUpClass('NSDictionary')()
    if not sys.platform == 'darwin':
        USE_NOTIFICATIONS = False
except:
    USE_NOTIFICATIONS = False
    nsd = False

# keyword arguments which will always be passed to notifier
NOTIFY_KWARGS = dict(sound=NOTIFY_SOUND,
                     nsd=nsd,
                     iconpath=iconpath,
                     switch=USE_NOTIFICATIONS)

# mapping unique id to result in an easy way. if it's too hard on memory, revise
ID_RES = OrderedDict()
QUERY_ID = OrderedDict()

# map corpus name to f-s indexed trees
CORPUS_TREES = defaultdict(dict)

# store a list of main searches
NON_EDITS = dict()

ALL_CORPORA = get_corpora_dict()

template_folder, static_folder, IN_MAC_APP = get_template_dir()

# initialise the app, and tell it about the upload folder
# add bootstrap support, add a csrf token for forms
kwargs = dict(template_folder=template_folder, static_folder=static_folder)
app = Flask(__name__, **kwargs)
app.json_encoder = JEncoder
app.config['UPLOAD_DIR'] = UPLOAD_DIR
Bootstrap(app)

# todo: just make this a random string
try:
    app.secret_key = get_secret_key()
    csrf = CSRFProtect(app)
except:
    pass


#  app.template_folder = os.path.join(os.path.abspath('.'), 'templates')
def allowed_file(filename):
    """
    Make sure uploaded file is safe
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class ParseForm(FlaskForm):
    """
    Form for parsing
    """
    lang = RadioField('Language', choices=[
        ('english', 'english'),
        ('german', "german"),
        ('arabic', 'arabic'),
        ('chinese', 'chinese'),
        ('french', 'french'),
        ('spanish', 'spanish'),
    ], default='english')

    metadata = BooleanField('XML metadata', description='XML metadata')
    #  coref = BooleanField('Coref', description='Coreferences')
    speaker = BooleanField('Speaker segmentation', description='Speaker names')
    projname = TextField('Project name', description="Name for the project")
    desc = TextField('Description', description="Description of the data")
    txt = FileField(validators=[FileRequired()])
    #  submit_button = SubmitField('Parse')


def identify_search(target=False, query=False, qstring=False, case_sensitive=False, inverse=False):
    """
    Get what we need from the query history for display
    """
    if not target and not qstring and isinstance(query, str):
        return query if len(query) < 70 else query[70] + '...'
    quotea, quoteb = "'", "'"
    base = " {}{} {}matching: <span class='querystring' style='font-family: Fira Code;'>{}{}{}</span>"
    no = 'not ' if inverse else ''
    case = 'case sensitive' if case_sensitive else ''
    query = getattr(query, 'pattern', query)
    if target in {'t', 'd'} and not qstring:
        target = query[0]
    if target == 'd':
        qtext = qstring
        qtext = qtext if len(qtext) < 70 else qtext[70] + '...'
        return base.format(case, 'Dependencies', no, quotea, qtext, quoteb)
    elif target == 't':
        qtext = qstring
        qtext = qtext if len(qtext) < 70 else qtext[70] + '...'
        return base.format(case, 'Trees', no, quotea, qtext, quoteb)
    else:
        if isinstance(query, list):
            quotea, quoteb = '[', ']'
            query = ', '.join(query)
        query = query if len(query) < 70 else query[70] + '...'
        if len(target) == 1:
            target = SHORT_TO_LONG_SHOW.get(target)
            if target.lower() not in ['pos', 'ner']:
                target = target.lower()
        elif len(target) == 2:
            if target in GOV_ATTRS:
                target = target.lstrip('g')
                tran = SHORT_TO_LONG_SHOW.get(target)
                if tran != 'POS':
                    tran = tran.lower()
                target = 'Governor ' + tran
            else:
                target = SHORT_TO_LONG_SHOW.get(target)
        return base.format(case, target, no, quotea, query, quoteb)


def get_previous(highlight_num):
    """
    Make a list of dicts of previous results, so that we can generate a table.
    Some formatting for jinja2 is here as well.

    Args:
        highlight_num: the id of the result to make active (i.e. most recent)

    Return:
        list: each item is a dict containing formatting instructions for the
        template. The goal is that the most recent query is active, its parent
        uncollapsed, and all other parents collapsed and inactive. older edits
        are disabled.
    """
    # here we store all our json like data
    out = []

    # if no previous searches, or user wants a new search, highlight new search
    if not ID_RES or highlight_num == 0:
        newsearch_active = "active"
    else:
        newsearch_active = ""

    # a dict entry for new search
    new_q_dict = {'id': 0,
                  'sstring': "Corpus: %s" % CurrentState.corpus_name,
                  'icon': "glyphicon glyphicon-globe",
                  'active': newsearch_active,
                  'searchnum': 0}
    out.append((new_q_dict, []))

    # if no results, just show new search
    if not ID_RES:
        return out

    # iterate over results, building dict values
    for i, edit_ids in NON_EDITS.items():
        r, meta, json_data = ID_RES[i]
        # uncollapsed main entries by default
        main_icon = "glyphicon glyphicon-chevron-right"
        edits = []
        sstring = identify_search(**meta.get('query', {}))

        # if this search is to be highlighted, make it active
        # and change the arrow to down if there are any edits
        if meta['id'] == highlight_num:
            main_active = 'active'
            main_in = 'in'
            if edit_ids:
                main_icon = 'glyphicon glyphicon-chevron-down'
        # if it isn't selected, keep it collapsed
        else:
            main_active = ""
            main_in = ""

        # for subsequent edits, do much the same thing
        for subi in edit_ids:
            subr, subm, subj = ID_RES[subi]
            # if this edit is to be highlighted, make active
            # and uncollapse parent
            if subm['id'] == highlight_num:
                active = 'active'
                main_in = 'in'
                main_icon = 'glyphicon glyphicon-chevron-down'
            else:
                active = ''
            # if one of the edits is most recent, but it's not this one, this
            # one should be disabled
            if highlight_num in edit_ids and not active:
                active = 'disabled'
            # if none of the edits in this branch are active, deactivate all
            # except the last one
            if highlight_num not in edit_ids and subi != edit_ids[-1]:
                active = 'disabled'

            subsstring = identify_search(**subm.get('query', {}))

            edits.append({'sstring': subsstring,
                          'id': subi,
                          'active': active,
                          "searchnum": subm['id']})
        out.append(({'sstring': sstring,
                     'id': i,
                     'icon': main_icon,
                     'active': main_active,
                     'in': main_in,
                     'searchnum': meta['id']}, edits))
    return out


class QueryForm(FlaskForm):
    """
    A search query form
    """
    corpus_name = False
    querystring = TextField('Query here', description='Query goes here')
    search_type = RadioField('Query language',
                             choices=[('Dependencies', 'Dependencies'),
                                      ('Trees', 'Trees'),
                                      ('natural', 'natural'),
                                      ('CQL', 'CQL')], default='Dependencies')
    case = BooleanField('Case sensitive', description='Case sensitive')
    inverse = BooleanField('Inverse', description='Inverse match')
    search_button = SubmitField('Search')
    #  searchfrom = TextField('searchfrom', description="Search from this")


def _make_list_query_list(qstring):
    if qstring.startswith('[') and qstring.endswith(']') and ',' in qstring:
        qstring = qstring.lstrip('[').rstrip(']')
        qstring = qstring.split(',')
    return [i.strip() for i in qstring]


def make_query(qstring, radio):
    """
    Take the user's query string and radio choice and make a dict for corpkit
    """
    kwargs = dict()
    if radio == 'Dependencies':
        target = 'd'
    elif radio == 'Trees':
        target = 't'
    elif radio == 'CQL':
        target = 'c'
    elif radio in get_metadata_fields(CurrentState.corpus_name):
        qstring = _make_list_query_list(qstring)
        target = radio
        kwargs['metadata_query'] = True
    elif radio.startswith('Governor '):
        qstring = _make_list_query_list(qstring)
        short = 'g' + radio.split(' ', 1)[1][0].lower()
        target = short
        return target, qstring, kwargs
    else:
        qstring = _make_list_query_list(qstring)
        rtrans = {v.lower(): k.lower() for k, v in SHORT_TO_LONG_SHOW.items()}
        feat = rtrans.get(radio.lower(), False)
        target = feat
    return target, qstring, kwargs


def get_corpus_info_for_mainpage():
    """
    Make the mainpage table
    """
    # after the first time, just return the already stored data
    if CurrentState.corpora_info:
        return CurrentState.corpora_info

    corpora_info = list()

    for name, obj in ALL_CORPORA.items():
        corpora_info.append(obj.metadata)

    CurrentState.corpora_info = corpora_info
    return corpora_info


@app.route('/annotate', methods=('GET', 'POST'))
def annotate():
    level = 'i' if request.form['wordsent'] else 's'
    field = request.form['field'].strip().replace('\t\n', '')
    if level == 'i':
        ANNOTATIONS[CurrentState.corpus_name].append(field)
    value = request.form['custom-text-box'].strip().replace('\t\n', '')
    if not value:
        value = request.form['anno-type'].strip().replace('\t\n', '')
        rtrans = {v.lower(): k.lower() for k, v in SHORT_TO_LONG_SHOW.items()}
        value = rtrans.get(value.lower(), value.lower())

    corpus = Corpus(CurrentState.corpus_name)
    corpus.tag(CurrentState.current_conc, field, value=value, level=level, dry_run=False)
    loaded = corpus.load()
    #  json_data = make_all_views_for(loaded, is_new=True, corp=loaded,
    #    cols=loaded.columns, **GLOBALS)
    ALL_CORPORA[CurrentState.corpus_name] = loaded
    # remaining problems:
    # still not loading the new corpus?
    # returns to search result but sentences are showing
    # pretty slow
    # zero feedback for the user on what the hell just happened

    return corpus_page(CurrentState.corpus_name)
    #  url = url_for('.corpus_page', corpus_name=CurrentState.corpus_name)
    #  return redirect(url)


@app.route('/upload_parse', methods=('GET', 'POST'))
def upload_parse():
    """
    Process the user's request to upload/parse
    """
    from corpkit.process import add_df_to_dotfile
    corpus_name = request.form['projname']
    corpus_name = corpus_name.replace('/', '-slash-').replace(' ', '_')
    f = request.files['txt']
    yt = request.form.get('youtube', '')
    if not allowed_file(f.filename) and not yt:
        raise ValueError("File must be txt, XML or srt.")
    secname = secure_filename(f.filename)
    parsed_path = os.path.join(CORPUS_DIR, corpus_name + '-parsed')
    raw_path = os.path.join(CORPUS_DIR, '_tmp', corpus_name)

    try:
        os.makedirs(raw_path)
    except OSError:
        pass

    if not yt.strip():
        f.save(os.path.join(raw_path, secname))

    lang = request.form.get('lang', 'English')
    if lang == 'Language':
        lang = 'English'

    parser = request.form.get('parse-parser', 'spaCy')
    parser = {'spaCy': 'spaCy',
              'Word features': 'features'}.get(parser, parser)

    # convert srt files
    if secname.endswith('.srt'):
        from corpkit.convert import srt_to_corpkit
        srt_to_corpkit(os.path.join(raw_path, secname))
        os.remove(os.path.join(raw_path, secname))

    if yt.strip():
        raise NotImplementedError

    corpus = Corpus(raw_path)

    do_met = 'metadata' in request.form or yt.strip() or secname.endswith('.srt')
    do_speak = 'speaker' in request.form

    if secname.endswith(('conll', 'conllu')):
        shutil.move(raw_path, parsed_path)
        parsed = Corpus(parsed_path)
        meta = parsed.metadata
    else:
        kwargs = dict(metadata=do_met,
                      speaker_segmentation=do_speak,
                      lang=lang.lower(),
                      parser=parser,
                      outpath=os.path.join(CORPUS_DIR),
                      NSDictionary=NOTIFY_KWARGS['nsd'],
                      iconpath=NOTIFY_KWARGS['iconpath'],
                      notify=NOTIFY_KWARGS['switch'])
        parsed = corpus.parse(**kwargs)
        meta = parsed.metadata
    desc = request.form.get('desc', False)
    add_df_to_dotfile(parsed.path, lang, typ='lang')
    if desc:
        add_df_to_dotfile(parsed.path, desc, typ='desc')
    # parsing is done ... now, load parsed data into memory
    nopar = parsed.name.replace('-parsed', '')
    parsed = parsed.load(load_trees=False)
    json_data = make_all_views_for(parsed,
                                   is_new=True,
                                   corp=parsed,
                                   cols=parsed.columns,
                                   current_ix=CurrentState.current_ix)
    ALL_CORPORA[nopar] = parsed
    CORPORA_JSON[nopar] = json_data

    # remove the plain one from ~/corpora
    shutil.rmtree(os.path.dirname(raw_path))
    return redirect(url_for('.corpus_page', corpus_name=nopar))


@app.route('/', methods=('GET', 'POST'))
def mainpage():
    """
    The main page
    """
    form = ParseForm()
    corpus_info = get_corpus_info_for_mainpage()
    # generate the upload form
    parse_pop = render_template(TEMPLATES['parse_pop'], form=form)
    # show the page
    return render_template(TEMPLATES['index'],
                           corpora=corpus_info,
                           parse_modal=parse_pop)


def form_update_string(selected_action, sels, kind):
    """
    Format a string that represents a table cutting action
    """
    if kind == 'conc':
        kind = 'concordance'
    s = selected_action
    if isinstance(sels, list):
        n = len(sels)
        pl = 'es' if n > 1 else ''
        s += ' %d match%s' % (n, pl)
    else:
        s += ' matches from'
        for k, v in sels.items():
            k = k + 's' if k in ['file', 'folder'] else k
            s += ' %d %s, ' % (len(v), k)
    return s.strip(', ') + ' (via %s)' % kind


@app.route('/preferences/<corpus>', methods=('GET', 'POST'))
def preferences(corpus):
    return render_template(TEMPLATES['preferences'])


@app.route('/update_result/<kind>', methods=('GET', 'POST'))
def update_result(kind):
    """
    Update a concordance or table
    """
    rtrans = {v.lower(): k.lower() for k, v in SHORT_TO_LONG_SHOW.items()}
    corpus_id = request.form.get('searchfrom', 0)
    corpus_name = CurrentState.corpus_name
    corp = CurrentState.corpus

    if int(corpus_id):
        res, meta, json_data = ID_RES[int(corpus_id)]
    else:
        res = corp
        #  json_data = CORPORA_JSON[corpus_name]

    is_new = kind == 'conc' and int(corpus_id) == 0

    # a space to hold generated keyword arguments for keyness/relative freq
    fmt_kwargs = {}

    # did the user want to sort?
    sort_by = request.form.get('viewer-sort', False)
    if sort_by:
        sort_by = sort_by.lower().split(' ', 1)[0]
        sort_by = sort_by.replace('alphabetical', 'name')
        if kind == 'table':
            fmt_kwargs['sort'] = sort_by

    ngram_slide = request.form.get('ngram-slider')
    if ngram_slide == '0,0':
        ngram = False
    else:
        ngram = [int(i) for i in ngram_slide.split(',')]
    fmt_kwargs['ngram'] = ngram

    # did the user select a new index or token format?
    subs = request.form.getlist('viewer-subcorpora[]')
    if kind == 'table' and subs:
        # translate the token attrs. this could be made safer...
        subs = [rtrans.get(x.lower(), x) for x in subs]
        fmt_kwargs['subcorpora'] = subs

    # todo: merge, skip or keep rows --- getSelections
    selected_action = request.form.get('viewer-rowselect-action', False)
    if selected_action == 'None':
        selected_action = False
    sels = request.form.get('selection', False)
    if sels:
        sels = json.loads(sels)
        if sels and kind == 'conc':
            sels = [int(i) for i in sels]
            rindex = list(res.index)
            sels = [rindex[i-1] for i in sels]

    # translate colour
    colour = request.form.get('viewer-conc-colour', False)
    if colour == 'None':
        colour = False
    if colour:
        fmt_kwargs['colour'] = colour.lower()[0]
    else:
        fmt_kwargs['colour'] = False

    # translate show
    show = request.form.getlist('viewer-features[]')
    if show:
        outshow = []
        for x in show:
            if x.startswith('Governor'):
                outshow.append('g' + x.split(' ', 1)[1][0].lower())
            else:
                outshow.append(rtrans.get(x.lower(), x))
        fmt_kwargs['show'] = outshow if outshow else False

    # translate rel freq/keyness
    relative = request.form.get('viewer-relative', False)
    if not relative:
        relative = False
    else:
        rel_type, denom = relative.split('-', 1)
        if denom == 'self':
            denom = True
        else:
            # some of this is automatic during table()
            # it also wastes time, could be in _json_data
            denom = ID_RES[int(denom)][0].table(**fmt_kwargs)
        fmt_kwargs[rel_type.lower()] = denom

    # if we are actually modifying the main result, update all views
    if sels and selected_action and int(corpus_id) != 0:
        # store buzzword data
        if isinstance(sels, dict):
            test = any(len(i) for i in sels.values())
        else:
            test = len(sels)
        if test:
            if selected_action == 'Keep':
                if kind == 'conc':
                    res = res.loc[sels]
                else:
                    # todo: delete method
                    raise NotImplementedError
                    res = res.just(metadata=sels)
            elif selected_action == 'Delete':
                if kind == 'conc':
                    res = res.drop(sels)
                else:
                    raise NotImplementedError
                    res = res.skip(metadata=sels)

            elif selected_action == 'Merge':
                for feat, vals in sels.items():
                    res = res.collapse(feat, vals, name=False)

            CurrentState.unique_ids += 1
            current_id = CurrentState.unique_ids
            newdict = dict(meta)
            newdict['id'] = current_id
            newdict['query'] = {'query': form_update_string(selected_action, sels, kind)}
            new_json_data = make_all_views_for(res,
                                               is_new=is_new,
                                               fmt_kwargs=fmt_kwargs,
                                               corp=corp,
                                               current_ix=CurrentState.current_ix)
            #todo
            #CurrentState.current_conc = start_from[['file', 's', 'i']].iloc[res.index].reset_index()[['file', 's', 'i', 'index']]
            new_json_data = add_previous(new_json_data, current_id)
            ancestor = get_ancestor_id(meta['id'])
            NON_EDITS[ancestor].append(current_id)
            ID_RES[current_id] = [res, newdict, new_json_data]
            return jsonify(new_json_data)

    dat = table_json(res,
                     is_new=is_new,
                     kind=kind,
                     corp=corp,
                     fmt_kwargs=fmt_kwargs,
                     current_ix=CurrentState.current_ix)
    if int(corpus_id):
        ID_RES[int(corpus_id)][2][kind] = dat
        ID_RES[int(corpus_id)][2]['needupdate'] = [kind]
        return jsonify(ID_RES[int(corpus_id)][2])
    else:
        CORPORA_JSON[corpus_name][kind] = dat
        CORPORA_JSON[corpus_name]['needupdate'] = [kind]
        return jsonify(CORPORA_JSON[corpus_name])


@app.route('/about')
def about():
    """
    An about page
    """
    return render_template(TEMPLATES['about'])


def generate_views(corpus_name, previous=False):
    """
    Make the data view for either search results or a corpus

    Args:
        corpus (Corpus): a corpus with available metadata
    """
    corpus_meta = []
    metadata = get_metadata_fields(corpus_name)
    for k in metadata:
        corpus_meta.append({'id': k, 'name': k, 'field': k, 'sortable': True})

    features = ['Index', 'Word', 'Lemma', 'XPOS', 'POS', 'Function',
                'Governor word', 'Governor lemma', 'Governor XPOS',
                'Governor POS', 'Governor function']
    rel = TEMPLATES['select_relative']
    viewer_relative = render_template(rel, prevdata=previous[1:])

    tree_modal = render_template(TEMPLATES['tree_modal'])
    chart_modal = render_template(TEMPLATES['chart_modal'])

    return render_template(TEMPLATES['viewer'],
                           tree_space=tree_modal,
                           chart_space=chart_modal,
                           corpus_metadata=corpus_meta,
                           features=features,
                           metadata=metadata,
                           viewer_relative=viewer_relative,
                           form=FlaskForm())


def get_ancestor_id(idx):
    """
    Figure out which search an interrogation came from
    """
    if not idx:
        return 0
    res, meta, j = ID_RES[idx]
    for x in range(99):
        if meta['parent_id'] == 0:
            return meta['id']
        else:
            res, meta, j = ID_RES[meta['parent_id']]
    raise ValueError('Stuck in a loop.')


@app.route('/view_different_result/<idx>', methods=('GET', 'POST'))
def view_different_result(idx):
    idx = int(idx)
    corpus_name = CurrentState.corpus_name
    if not idx:
        json_data = CORPORA_JSON[corpus_name]
    else:
        res, meta, json_data = ID_RES.get(idx)
    json_data['needupdate'] = ['conc', 'pivot', 'table', 'tree']
    return jsonify(json_data)


@app.route('/do_search', methods=('GET', 'POST'))
def do_search():
    """
    The user has searched or filtered the corpus
    """
    t0 = time.time()
    corpus_name = CurrentState.corpus_name

    # get the corpus the user wants to edit
    corpus_id = request.form['searchfrom'].strip()

    if not int(corpus_id):
        old_json_data = CORPORA_JSON[corpus_name]
        start_from = ALL_CORPORA[corpus_name]

        if type(start_from) == Corpus:
            start_from = start_from.load()
            ALL_CORPORA[corpus_name] = start_from
    else:
        # get the interrogation and metadata
        matches, meta, old_json_data = ID_RES.get(int(corpus_id))
        start_from = ALL_CORPORA[corpus_name].loc[matches.index]

    qstring = request.form['querystring']
    search_type = request.form['search_type']

    # reset the tree we're currently up to
    CurrentState.current_ix = False

    target, query, kwargs = make_query(qstring, search_type)

    # when the user searches metadata, show sentences unless it is a filter
    mq = kwargs.pop('metadata_query', False)
    metadata_query = False if int(corpus_id) else mq

    #  todo: allow the user to control this
    kwargs['case_sensitive'] = False

    kwargs['inverse'] = not request.form.get('inverse')

    # are we searching or filtering
    filtering = int(corpus_id) != 0

    if filtering:
        parent_id = meta['id']
    else:
        parent_id = 0

    # below we get all the query values together, and check if the query has
    # already been performed. if it has, we just return that view
    query_id_dict = dict(corpus_name=CurrentState.corpus_name,
                         editing=filtering,
                         parent_id=parent_id)

    query_id_dict.update(kwargs)
    query_id_dict.update({target: query})
    query_id_dict = tuple(sorted(query_id_dict))
    duplicate = QUERY_ID.get(query_id_dict, False)

    if duplicate:
        print('Query is a duplicate ... a modal should pop up here.', file=sys.stderr)
        return view_different_result(duplicate)

    # actually do search of corpus or previous result. this should be
    # the only time in the app that real searching is performed
    res = start_from.search(target=target, query=query, **kwargs)

    if res is None:
        print('No results ...', file=sys.stderr)
        flash('No results found, sorry.', 'error')
        return jsonify(old_json_data)

    # todo: speed up current conc shit
    # for level in ['file', 's', 'i']:
    #    if level not in res.columns:
    #        start_from[level] = start_from.index.get_level_values(level)
    # CurrentState.current_conc = start_from[['file', 's', 'i']].iloc[res.index].reset_index()[['file', 's', 'i', 'index']]

    # unique ids are used when the user switches views on previous pane
    CurrentState.unique_ids += 1
    current_id = CurrentState.unique_ids

    # ancestor is the id of the result whose parent is the corpus
    ancestor = get_ancestor_id(parent_id)

    # NON_EDITS stores a search id as key and list of its sub interrogations
    # so, we need to know the id of the non-edit this came from
    if filtering:
        NON_EDITS[ancestor].append(current_id)
    else:
        NON_EDITS[current_id] = []

    # store query and id, so duplicate queries can be caught
    QUERY_ID[current_id] = query_id_dict
    # put the result into our master dict of results

    qdict = dict(query=query,
                 target=target,
                 case_sensitive=kwargs['case_sensitive'],
                 qstring=getattr(res, 'qstring', False),
                 inverse=kwargs['inverse'])

    # store information regarding our search
    search_data = dict(id=current_id,
                       parent_id=parent_id,
                       app_query=query_id_dict,
                       query=qdict)

    ID_RES[int(current_id)] = [res, search_data, False]

    # make and store html json as early as possible
    # worth optimising
    json_data = make_all_views_for(res,
                                   is_new=metadata_query,
                                   corp=ALL_CORPORA[corpus_name],
                                   current_ix=CurrentState.current_ix)
    json_data = add_previous(json_data, current_id)

    ID_RES[int(current_id)][2] = json_data

    t1 = time.time()
    if NOTIFY_KWARGS['switch'] and t1 - t0 >= NOTIFY_MIN_TIME:
        numres = format(len(res), ',')
        secs = str(round(t1-t0, 2))
        comp_s = "%s results in %s sec." % (numres, secs)
        notifier(header="Search completed",
                 subheader='',
                 text=comp_s,
                 **NOTIFY_KWARGS)

    # send json back to the frontend for display
    return jsonify(json_data)


def add_previous(json_data, current_id):
    previous = get_previous(int(current_id))
    previous_space = render_template(TEMPLATES['query_history'], data=previous)
    json_data['previous'] = previous_space
    rel = TEMPLATES['select_relative']
    viewer_relative = render_template(rel, prevdata=previous[1:])
    json_data['table_extra'] = viewer_relative
    json_data['needupdate'] += ['table_extra', 'previous']
    return json_data


def get_metadata_fields(corpus_name):
    """
    Get all metadata fields
    """
    cols = list(ALL_CORPORA[corpus_name].columns)
    extra = ['parse', 'text', 'sent_id']
    l = [i.strip() for i in cols if i.strip() not in CONLL_COLUMNS_V2 + extra]
    if ANNOTATIONS[corpus_name]:
        l = ANNOTATIONS[corpus_name] + l
    if 'file' not in l:
        l.append('file')
    return l


def has_parse_trees(corpus_name):
    """
    Figure out if corpus is parsed
    """
    return 'parse' in ALL_CORPORA[corpus_name].columns


def categorical(df):
    """
    Make categories on a DataFrame

    todo: consider adding check for w/l columns: very long, don't categorise
    """
    if any(i.name == 'category' for i in df.dtypes):
        print("Already categorised...", file=sys.stderr)
        return df

    for k, v in DTYPES.items():
        if k in df.columns:
            print(CurrentState.corpus_name, k, file=sys.stderr)
            try:
                df[k] = df[k].astype(v)
            except KeyboardInterrupt:
                raise
            except:
                pass
    return df


@app.route('/explore/<corpus_name>', methods=('GET', 'POST'))
def corpus_page(corpus_name):
    """
    Main display page for a corpus

    Args:
        corpus_name (str): name of the corpus
    """
    CurrentState.corpus_name = corpus_name
    corpus = ALL_CORPORA[corpus_name]

    # for super lazy loading, we can just link for now to the corpus name
    CurrentState.corpus = corpus_name

    if isinstance(ALL_CORPORA[corpus_name], Corpus):
        ldd = ALL_CORPORA[corpus_name].load()
        ALL_CORPORA[corpus_name] = ldd

    # load the data for this corpus as quickly as possible
    json_data = CORPORA_JSON[corpus_name]

    # we could have way too many conc lines...
    conc_data = json_data['conc']['data'][:MAX_CONC_ROWS]
    json_data['conc']['data'] = conc_data

    metadatas = get_metadata_fields(corpus_name)
    pt = has_parse_trees(corpus_name)

    # feature corpora are different from corenlp corpora
    if 'parser' in metadatas:
        cols = [i for i in list(corpus.columns) if i not in ['w', 'l', 'x', 'p']]
        features = ['Word', 'Lemma', 'XPOS', 'POS'] + cols
    else:
        features = ['Index', 'Word', 'Lemma', 'XPOS', 'POS', 'Function']

    kwargs = dict(form=FlaskForm(), features=features, metadatas=metadatas)
    annotate_pop = render_template(TEMPLATES['annotate_pop'], **kwargs)

    # make the query form, with dropdowns for the metadata and features
    query_space = render_template(TEMPLATES['query_form'], parse_trees=pt, **kwargs)

    # get the search history list with proper active, collapse, etc
    # since we've performed a search, we want to highlight the latest id
    previous = get_previous(CurrentState.unique_ids)
    previous_space = render_template(TEMPLATES['query_history'], data=previous)
    # generate the data views
    viewer_space = generate_views(corpus_name, previous=previous)

    return render_template(TEMPLATES['explore'],
                           query_space=query_space,
                           previous_space=previous_space,
                           viewer_space=viewer_space,
                           error=None,                      # not working yet
                           corpus_name=corpus_name,
                           initial_data=json_data,
                           annotate_modal=annotate_pop)


@app.route("/view_tree/<corpus>/<move>", methods=["GET",  "POST"])
def _tree_json(corpus, move, *args, **kwargs):
    """
    Load or build the json needed for a displacy tree

    Return:
        Response/json
    """
    # res specifies the id of the result set we want to view,
    # or zero for the corpus itself
    corpus = int(corpus)
    corp = ALL_CORPORA[CurrentState.corpus]

    if not corpus:
        corpus = corp
        is_new = True
    else:
        corpus, meta, json_data = ID_RES[corpus]
        is_new = False

    tree, cons, ix = tree_json(corpus,
                               move=move,
                               is_new=is_new,
                               corp=corp,
                               current_ix=CurrentState.current_ix)
    CurrentState.current_ix = ix
    return jsonify({'tree': tree, 'cons': cons})


@app.route("/clear_search_history/<corpus_name>", methods=["GET",  "POST"])
def clear_search_history(corpus_name, ret=True):
    """
    Delete all results from memory
    """
    ID_RES.clear()
    NON_EDITS.clear()
    CurrentState.unique_ids = 0
    if ret:
        return corpus_page(corpus_name)


def run(*args):
    """
    Start the app and open a browser window containing it
    """
    import threading

    kwargs = cmd_line_to_kwargs(args)

    if 'port' not in kwargs:
        kwargs['port'] = 5555

    url = 'http://127.0.0.1:{0}'.format(kwargs['port'])
    bank = kwargs.pop('bank', False)
    if bank:
        url += '/explore/' + bank

    serve = kwargs.pop('serve', False)
    if not serve:
        threading.Timer(1.25, lambda: webbrowser.open(url, new=1)).start()

    app.run(threaded=True, use_reloader=False, **kwargs)

##################
# START MENULET
##################


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, menulet, **kwargs):
        super(StoppableThread, self).__init__(**kwargs)
        self._stop_event = threading.Event()
        self._menulet = menulet

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


try:
    import rumps

    class BuzzwordMenulet(rumps.App):
        """
        A menulet wrapper for buzzword
        """

        def __init__(self, *args):
            """
            Start the app and menulet
            """
            notifier('Initialising buzzword...', '', '', **NOTIFY_KWARGS)
            ic = NOTIFY_KWARGS['iconpath']
            super(BuzzwordMenulet, self).__init__('buzzword', icon=ic, quit_button=None)

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.buzzword = False
            self.running = sock.connect_ex(('127.0.0.1', PORT))
            self.url = 'http://127.0.0.1:{}'.format(PORT)
            self.args = args
            # if port is busy, just open a browser there
            if self.running == 0:
                webbrowser.open(self.url)

            # if port not busy, open buzzword and browser
            else:
                self.start()
            self.run()

        def start(self):
            """
            Start the flask part of the app in a separate thread
            """
            self.buzzword = StoppableThread(self,
                                            name='buzzword',
                                            target=run,
                                            args=self.args)
            self.buzzword.start()

        def stop(self):
            """
            Try many methods to kill the thread/subprocess
            This can be fixed when the threading method is stable.
            """
            self.buzzword._stop = True
            if self.buzzword:
                for method in ['kill', 'terminate', 'exit', 'stop']:
                    try:
                        getattr(self.buzzword, method, 'stop')()
                    except:
                        pass

        @rumps.clicked("Preferences")
        def prefs(self, _):
            name = CurrentState.corpus_name or 'General'
            page = self.url + '/preferences/{}'.format(name)
            webbrowser.open(page)
            #  rumps.alert("Not done yet.", **NOTIFY_KWARGS)

        @rumps.clicked('Open')
        def _open(self, _):
            webbrowser.open(self.url)

        @rumps.clicked('Restart')
        def restart(self, _):
            notifier("Restarting buzzword...", "", "", **NOTIFY_KWARGS)
            self.stop()
            self.start()

        @rumps.clicked('Quit')
        def clean_up_before_quit(self, _):
            self.stop()
            rumps.quit_application()

except ImportError:
    BuzzwordMenulet = None


if __name__ == "__main__":
    menu_ok = can_use_rumps(sys.argv)
    args = [i for i in sys.argv if 'nomenu' not in i]
    if menu_ok:
        app = BuzzwordMenulet(*args)
    else:
        run(*args)
