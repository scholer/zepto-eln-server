

"""

Module for dealing with `Pico` markdown stuff, mostly just %variable% substitution.

"""

import re
from collections import defaultdict

NODEFAULT = object()


def pico_find_variable_placeholders(content, pat=r"%[\w\.]+%"):
    if isinstance(pat, str):
        pat = re.compile(pat)
    print("type(content):", type(content))
    res = pat.findall(content)
    print("type(res):", type(res))
    return set(res)  # Set to remove duplicates


def get_attrs_string_value(dct, attrs, default=NODEFAULT):
    """ Get attribute from object string: dict.key1.subkey2.subsubkey

    Args:
        dct:
        attrs: A string 'attr0.attr1.attr2' or list ['attr0', 'attr1', 'attr2']
        default: A default value if the given attrs string wasn't found.
            If no default is given, a KeyError is raised.

    Returns:
        The value given by attrs.

    Examples:
        >>> a = {'h': {'e': {'j': 'word'}}}
        >>> get_attrs_string_value(a, 'h.e.j')
        'word'

    """
    if isinstance(attrs, str):
        attrs = attrs.split('.')
    key, *rest = attrs
    try:
        val = dct[key]
    except TypeError:
        val = getattr(dct, key)
    except KeyError as exc:
        if default is not NODEFAULT:
            return default
        else:
            raise exc
    if rest:
        return get_attrs_string_value(val, attrs=rest, default=default)
    else:
        return val


def substitute_pico_variables(content, template_vars, errors='pass', varfmt="{sub}"):
    """ Perform Pico-style %variable% substitution. """
    # variable members are available as %variable.attribute%
    # Two approaches:
    #   a. Extract variables from document and substitute them. [we use this one]
    #   b. Generate all possible variable placeholder strings and do str.replace(placeholder, value).
    placeholders = pico_find_variable_placeholders(content)
    if isinstance(varfmt, str):
        _varfmt = varfmt
        varfmt = defaultdict(lambda: _varfmt)
    for placeholder in placeholders:
        # Note: We probably shouldn't do replacements inside comments, but whatever.
        varname = placeholder.strip('%')
        try:
            sub = get_attrs_string_value(template_vars, varname)
        except KeyError as exc:
            # E.g. if you have a comment explaining %meta.variable%:
            if errors == 'raise':
                raise exc
            elif errors == 'print':
                print(f"{exc.__class__.__name__}: {exc}")
            elif errors == 'pass':
                pass
            else:
                raise ValueError(f"Value {errors!r} for parameter `errors` not recognized.")
        else:
            print(f"Replacing {placeholder!r} -> {sub!r}")
            # sub can be e.g. lists or dicts; the format string can be customized for each variable.
            content = content.replace(placeholder, varfmt[varname].format(sub, var=sub, sub=sub))
    return content


def document_substitute_pico_vars(document):
    # Perform %pico_variable% substitution:
    pico_vars = document.copy()
    pico_vars.update(document['fileinfo'])  # has 'dirname', 'basename', etc.
    document['content'] = substitute_pico_variables(document['content'], template_vars=pico_vars, errors='print')
