

"""

See notes/templating.md


"""

import os
import sys
import pathlib
import glob
from pprint import pprint


def apply_template_file_to_document(
        document, template_type='jinja2', template=None, template_dir=None, default_template_name='index',
        template_vars=None,
):
    """ Locate the proper template file to use and apply it to the document.

    Args:
        document:
        template_type:
        template:
        template_dir:
        default_template_name:

    Returns:
        html (str) and also updates document['html'] in-place.

    See also:


    """
    if template_vars is None:
        template_vars = {}
    print("\nApplying template file to document...")
    print(" - template_dir:", template_dir)

    if template is None or not os.path.isfile(template):  # and template_dir is not None:
        # Template can be e.g. 'ProjectTemplate', which should map to the 'ProjectTemplate' template in template_dir.
        print("\n(template is None or not os.path.isfile(template)) and template_dir is not None.\n", file=sys.stderr)
        if template is None:
            template_name = document['meta'].get('template', default_template_name)
            print(f"No template given, using template name from YFM (or default): {template_name!r}.", file=sys.stderr)
        else:
            template_name = template
        print(f"Locating template {template!r} in template_dir {template_dir!r}.")
        assert template_dir is not None
        assert os.path.isdir(template_dir)
        template_selection = get_templates_in_dir(template_dir, glob_patterns=("*.jinja",))
        # glob_patterns=("*.html", "*.j2.html", "*.j2", "*.twig"))
        try:
            template = template_selection[template_name]
        except KeyError:
            raise FileNotFoundError(
                f"WARNING: Template_dir does not contain any templates matching {template_name!r} (case sensitive).")
        else:
            print(f"Using template {template_name!r} from template directory {template_dir!r}.", file=sys.stderr)

    print("Applying template:", template)
    template_vars.update(document)
    template_vars['content'] = document['html_content']  # Default document "content" entry is the Markdown.
    html = apply_template(template=pathlib.Path(template), template_type=template_type, template_vars=template_vars)
    document['html'] = html
    return html


def apply_template(template, template_vars, template_type='jinja2'):
    """

    Args:
        template:
        template_vars:
        template_type:

    Returns:

    See also:

        >>> flask.render_template(template, template_vars)

    """
    if isinstance(template, pathlib.Path):
        template = open(template, encoding='utf-8').read()

    print("Performing template variable subsubstitution...", file=sys.stderr)
    # Twig/Jinja template interpolation:

    if template_type.startswith('jinja'):
        import jinja2
        print("template length:", len(template))
        template = jinja2.Template(template)
        html = template.render(**template_vars)
    else:
        raise ValueError(f"Value {template_type!r} for `template_type` not recognized.")

    return html


def get_templates_in_dir(template_dir, glob_patterns=('*.jinja',)):

    files = [fn for pat in glob_patterns for fn in sorted(glob.iglob(os.path.join(template_dir, pat)))]
    print(f"\nTemplate files in {template_dir!r}:", file=sys.stderr)
    print("\n".join(f" - {fn!r}" for fn in files), file=sys.stderr)

    templates_by_name = {os.path.splitext(os.path.basename(fn))[0]: fn for fn in files}
    templates_by_name.update({fn: fn for fn in files})
    pprint(templates_by_name)

    return templates_by_name