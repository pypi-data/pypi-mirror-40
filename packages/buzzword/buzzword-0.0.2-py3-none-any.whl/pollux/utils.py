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
