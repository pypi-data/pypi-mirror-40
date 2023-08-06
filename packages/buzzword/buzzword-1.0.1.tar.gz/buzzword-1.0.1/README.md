buzzword: text analysis app
===========================

<!--- Don't edit the version line below manually. Let bump2version do it for you. -->
> Version 1.0.1

[![DOI](https://zenodo.org/badge/14568/interrogator/buzzword.svg)](https://zenodo.org/badge/latestdoi/14568/interrogator/buzzword) [![Travis](https://img.shields.io/travis/interrogator/buzzword.svg)](https://travis-ci.org/interrogator/buzzword) [![PyPI](https://img.shields.io/pypi/v/buzzword.svg)](https://pypi.python.org/pypi/buzzword) [![ReadTheDocs](https://readthedocs.org/projects/buzzword/badge/?version=latest)](http://buzzword.readthedocs.org/en/latest/) [![Docker Automated build](https://img.shields.io/docker/automated/interrogator/buzzword.svg)](https://hub.docker.com/r/interrogator/buzzword/) [![Anaconda-Server Badge](https://anaconda.org/asmeurer/conda/badges/installer/conda.svg)](https://anaconda.org/interro_gator/buzzword)

buzzword is a web application and backend for a bunch of overlapping fields/tasks:

- text analysis
- corpus linguistics
- treebank research
- distant reading
- digital humanities


It performs:

- Parsing
- Searching
- Result editing
- Data vis
- Concordancing
- Keywording
- Parse tree/dependency viewing

It is designed with **parsed**, **metadata-rich** corpora in mind, doing more sophisticated linguistic work than current tools, with a modern web interface, and a solid API.

The frontend is written in Bootstrap. The backend is [buzz](https://www.github.com/interrogator/buzz), a radically altered fork of the now deprecated [corpkit](https://www.github.com/interrogator/corpkit).

Install
=========

Before installing buzzword into **a Python 3 environment**, you should try to install [HDF5](https://support.hdfgroup.org/HDF5/release/obtainsrc.html), a library for high performance data storage. It isn't strictly necessary, but some things will be much faster.

After that, installing buzzword is pretty simple.

```bash
# virtual environment use is encouraged
pip install buzzword
```

Or, via Git:

```bash
git clone https://github.com/interrogator/buzzword
cd buzzword
python setup.py install
```

Quickstart
============

After installation, the following command will download and index a sample corpus of English, and load it in buzzword:

```bash
buzzword-quickstart
```

Make corpora
=============

Now that you have buzzword set up, you'll need some data. Data is simply a folder containing text files. Currently, English, German, Arabic, Chinese, Spanish and French are supported. Your text files can be in subfolders, representing subcorpora.

Your data can either be plain text, or plain text plus metadata. All metadata will be ignored during parsing, but added to the data later, so that you can search it, filter it, and so on.

Metadata can be specified through XML tags at the end of lines:

```
I hope everyone is hanging in with this blasted heat. As we all know being hot, sticky,
stressed and irritated can bring on a mood swing super fast. So please make sure your
all takeing your meds and try to stay out of the heat. <metadata speaker="Emz45" 
totalposts="5063" currentposts="4051" date="2011-07-13" postnum="0" threadlength="1">
```

If you only have speaker IDs, your data can also be formatted like a script:

```
Emz45: I hope everyone is hanging in with this blasted heat ...
FaanG: Barely, but i am!
```

Your data can have both speaker IDs and XML metadata, but if that's the case, perhaps just create a metadata attribute called `speaker`.

Once you have plain or metadata-added corpora, there are two ways to get the data parsed. First, if you're not much of a programmer, you can open the app by typing `buzzword` into your terminal, and by clicking `Upload` in the app. **Right now this will not give you any progress information, and needs more testing.**

You can also parse and add corpora to buzzword with a couple of simple commands.

```bash
buzzword-parse path/to/corpus
```

The command takes a number of arguments:

| Argument | Type  | Purpose  |
|---|---|---|
| `--speaker-segmentation`  | Flag | Corpus has speaker names  |
| `--metadata`  | Flag | Corpus has XML metadata  |
| `--coref`  | Flag  | Also do coreference resolution and some morphological features  |
| `--restart`  | Flag  | Do not overwrite existing files  |
| `--multiprocess=n`  | integer  | Parse files in parallel  |
| `--memory-mb=n`  | integer  | Memory for parser in megabytes  |

This creates a parsed version of the corpus, `path/to/corpus-parsed`, containing CONLL-U format files, which look like this:

```
# sent_id 1
# parse=(ROOT (S (NP (PRP I)) (VP (VBP hope) (SBAR (S (NP (NN everyone)) (VP (VBZ is) (VP (VBG hanging) (PP (IN in) (IN with) (NP (DT this) (VBN blasted) (NN heat)))))))) (. .)))
# speaker=Emz45
# threadlength=1
# currentposts=4051
# date=2011-07-13
# year=2011
# postnum=0
1   I         I         PRP O   2   nsubj      0       1
2   hope      hope      VBP O   0   ROOT       1,5,11  _
3   everyone  everyone  NN  O   5   nsubj      0       _
4   is        be        VBZ O   5   aux        0       _
5   hanging   hang      VBG O   2   ccomp      3,4,10  _
6   in        in        IN  O   10  case       0       _
7   with      with      IN  O   10  case       0       _
8   this      this      DT  O   10  det        0       2
9   blasted   blast     VBN O   10  amod       0       2
10  heat      heat      NN  O   5   nmod:with  6,7,8,9 2*
11  .         .         .   O   2   punct      0       _
```


Next, move it into a dedicated storage folder, `~/corpora`:

```bash
mkdir ~/corpora
mv path/to/corpus-parsed ~/corpora
```
 
You can do this for as many corpora as you like. When you've added all the corpora you need to `~/corpora`, run the command below to create high-performance versions of them:

```bash
buzzword-build
```

Run buzzword
=============

Once you've created a high-performance database (in `~/corpora/corpora.h5`), you can simply enter `buzzword` into the terminal to launch the app.

Using the app
==============

So far undocumented, sorry.

Backend
==========

The backend is the most mature part of the tool. Here's an example:

```python
>>> from buzz import Corpus
# load raw corpus
>>> data = Corpus('path/to/corpus')
# parse corpus
>>> parsed = data.parse(speaker_segmentation=True)
# search dependencies
>>> doers = parsed.deps(r'f/nsubj/ <- p/^VB.*/')
# make table from results
>>> doers.table(subcorpora='year', show=['w', 'l'], relative=True)
```

```python
# generate concordance
>>> doers.conc(show=['w', 'p'])
```

There is also a `matplotlib` interface:

```python
>>> doers.visualise("Doers by year", kind='area', num_to_plot=5)
```

Documentation coming soon.

More information
=================

There's still a lot to do!

[Emerging docs](http://buzzword.readthedocs.io/)

[Roadmap](https://github.com/interrogator/buzzword/blob/master/roadmap.md)

[Tweet @interro_gator](https://twitter.com/interro_gator)