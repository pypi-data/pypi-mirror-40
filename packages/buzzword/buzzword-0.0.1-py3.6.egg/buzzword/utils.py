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



def determine_corpus(name_or_df,
                     search=False,
                     is_new=False,
                     matches=False,
                     need_sents=False,
                     store_path='~/corpora/corpora.h5',
                     case_sensitive=False):
    """
    Give the user the minimum-memory object from which they can search,
    but return a high-memory object if it was passed in

    Return: DataFrame to search from
    """
    # if we were given a corpus and don't have to cut it down
    if not isinstance(name_or_df, str) and matches is False:
        return name_or_df
    # cut down an in memory corpus and return it
    elif not isinstance(name_or_df, str) and matches is not False:
        return name_or_df.iloc[matches.index]

    # otherwise, we have to go to the store
    storepath = os.path.expanduser(store_path)
    try:
        hdf = pd.HDFStore(storepath)
    except ImportError:
        raise ValueError("You need HDF5 installed for this.")

    # not sure we should ever get here, for for new corpora, return each sentence once
    if is_new:
        return hdf.select(name_or_df, 'i=1')

    # if we are dep searching, we try to cut down by inspecting the query, getting
    # the first part, and returning only those sents
    if search and search.get('d'):
        depgrep_string, search, offset = preprocess_depgrep(search, case_sensitive)

    if matches is not False:
        if not search:
            search = {}
        if 'd' not in search and not need_sents:
            mats = list(matches.index)
            return hdf.select(name_or_df, 'index in mats')

        # revise this, faster mask needed
        fsi = hdf.select(name_or_df, columns=['file', 's', 'i']).set_index(['file', 's', 'i'])
        if need_sents or 'd' in search:
            mask = fsi.droplevel('i').isin(set(matches.index.droplevel('i')))
        else:
            mask = fsi.isin(set(matches.index))
        return hdf.select(name_or_df, where=mask)

    if search is False:
        return hdf[name_or_df]

    ob, att = next((k, v) for k, v in search.items() if k != 'd')

    # get a list of the relevant categories
    try:
        poss_vals = list(hdf.select(name_or_df, 'columns=ob')[ob].cat.categories)
    except AttributeError:
        poss_vals = list(set(hdf.select(name_or_df, 'columns=ob')[ob]))
    if isinstance(search, list):
        good_ones = [i for i in poss_vals if i in att]
    else:
        good_ones = [i for i in poss_vals if re.search(att, i)]

    # get sents, cut down
    if 'd' in search or need_sents:
        ix = hdf.select(name_or_df, columns=["file", "s", "i"]).index
        fs = ix.droplevel('i')
        matches = hdf.select(name_or_df, '%r=good_ones' % ob, columns=['file', 's', 'i', ob])
        matches = matches.index.droplevel('i').unique()
        mask = fs.isin(set(matches))
        return hdf.select(name_or_df, where=mask)
    else:
        return hdf.select(name_or_df, '%r=good_ones' % ob)
