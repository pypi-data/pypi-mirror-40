import os
import sys
from .config import CORPUS_DIR, MEMORY
from .constants import APP_STRING
from buzz import Corpus
import buzzword


def cmd_line_to_kwargs(args):
    """
    Turn bash-style command lin arguments into Python kwarg dict
    """
    trans = {'true': True,
             'false': False,
             'none': None}

    kwargs = dict()
    for index, item in enumerate(args):
        if item.startswith('-'):
            item = item.lstrip('-').replace('-', '_')
            if 'bank' not in item:
                item = item.lower()
            if '=' in item:
                item, val = item.split('=', 1)
            else:
                try:
                    val = args[index+1]
                except IndexError:
                    val = 'true'
            if val.startswith('-'):
                val = 'true'
            val = val.strip()
            if val.isdigit():
                val = int(val)
            if isinstance(val, str):
                if val.startswith('-'):
                    continue
                val = trans.get(val.lower(), val)
            kwargs[item] = val
    return kwargs


def get_template_dir():
    """
    Correct the paths if inside a .app, potentially .exe
    """
    if APP_STRING in buzzword.__file__:
        fdir = buzzword.__file__.split(APP_STRING)[0]
        template_folder = os.path.join(fdir, 'Contents/MacOS/templates')
        static_folder = os.path.join(fdir, 'Contents/MacOS/static')
        IN_MAC_APP = True
    else:
        template_folder = 'templates'
        static_folder = 'static'
        IN_MAC_APP = False
    return template_folder, static_folder, IN_MAC_APP


def get_corpora_dict():
    """
    Map corpus names to corpus objects based on memory setting
    """
    name_to_corpus = dict()

    for d in os.listdir(CORPUS_DIR):
        if d in {'_tmp', 'uploads'}:
            continue
        if os.path.isfile(os.path.join(CORPUS_DIR, d)):
            continue
        corpus = Corpus(os.path.join(CORPUS_DIR, d))
        if MEMORY == 'buzz':
            corpus = corpus.load()
        name = d.replace('-parsed', '')
        name_to_corpus[name] = corpus

    if MEMORY in {'disk', 'buzz', 'onclick'}:
        return name_to_corpus

    raise NotImplementedError('Unknown memory option: {}'.format(MEMORY))


def notifier(header='', subheader='', text='', iconpath=None, nsd=False, sound=False, switch=False):
    """
    Cross platform alerts ... only macOS done so far.
    """
    if not switch:
        return
    if sys.platform == 'darwin':
        import rumps
        kwa = dict(data=nsd, sound=sound, img=iconpath)
        rumps.notification(header, subheader, text, **kwa)
    else:
        #  todo if possible on other os
        pass


def can_use_rumps(args):
    # check that the user hasn't specified no menu
    if any(i.lstrip('-').startswith('nomenu') for i in args):
        return False
    # check that we're on macOS
    if sys.platform != 'darwin':
        return False
    # check that we have the correct dependencies
    try:
        import rumps
        import objc
    except ImportError:
        return False
    # if all checks pass, allow notification center
    return True
