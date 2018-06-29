

"""




Templating systems:
-------------------

Overview:
* Jinja2 (Python) - by the Pocoo team (Flask, Sphinx, Pygments).
* Django template system (on which Jinja was modelled). Uses `{{` tags and `{%` blocks. Python.
* Twig (PHP) - uses a similar syntax to Django/Jinja, using `{{` tags and `{%` blocks.
    By Fabien Potencier (Symfony author) and Armin Ronacher (Jinja author).
* Liquid (Ruby) - Another Django-inspired templating language. For Ruby.
* Mustache - Also uses {{ curly }} braced syntax, but "Logic-less templating language".
* Handlebars - extension of Mustache, originally JS.
* Nunjucks - JS, similar to Jinja2.
* Velocity - Java originating templating engine. Apache project.
* Mako - Another popular Python templating language, using `<%` tags and `%` blocks.
* Cheetah - Uses '#' line prefix and '$' variables, like Velocity. Very similar to writing Python code.
* Genshi
* Hiccup, Sneeze
* Template Attribute Language (TAL)
* HAML, JADE, Pug - Alternative "languages" to write the DOM.
* Python-based templating: %s interpolation, {} formatting, and $ templating.
*

Note: Pico has two ways of injecting variables:
    1. Pico variables, where %metadata_variables% are replaced, at the Markdown level.
    2. Twig variables, which operates at the HTML level.
        {{html_content}} is the variables that inserts the markdown-converted html into the page body.

Typical extensions:
* *.jinja2 (or just *.j2), *.twig, etc.
* Can be single, *.jinja2, or *.html.jinja2 - similar to *.tar.gz.
*


Refs:
* http://vschart.com/list/template-language/
* http://jinja.pocoo.org/docs/2.10/switching/
* https://en.wikipedia.org/wiki/Comparison_of_web_template_engines
* https://www.quora.com/Was-Twigs-syntax-inspired-by-Liquid


Jinja templating:
-----------------

Refs:
* http://flask.pocoo.org/docs/1.0/quickstart/#rendering-templates
* http://flask.pocoo.org/docs/1.0/tutorial/templates/
* http://flask.pocoo.org/docs/1.0/templating/


Flask templating (uses Jinja):
-------------------------------


Q: How to change the template directory?
* A: Just pass `template_folder` when instantiating your Flask app: `Flask(__name__, template_folder="wherever")`

Q: How to change template directory dynamically?
* https://stackoverflow.com/questions/13598363/how-to-dynamically-select-template-directory-to-be-used-in-flask
* You can overwrite the `app.jinja_loader`, and use a `jinja2.ChoiceLoader` object:
```
app.jinja_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(['/flaskapp/userdata',
                                 '/flaskapp/templates']),
    ])
```



"""

import os
import sys
import pathlib
import glob
from pprint import pprint


def apply_template_file_to_document(
        document, template_type='jinja2', template=None, template_dir=None, default_template_name='index',
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
        template_selection = get_templates_in_dir(template_dir, glob_patterns=("*.html", "*.j2.html", "*.j2", "*.twig"))
        try:
            template = template_selection[template_name]
        except KeyError:
            raise FileNotFoundError(
                f"WARNING: Template_dir does not contain any templates matching{template_name!r} (case sensitive).")
        else:
            print(f"Using template {template_name!r} from template directory {template_dir!r}.", file=sys.stderr)

    print("Applying template:", template)

    html = apply_template(template=pathlib.Path(template), template_type=template_type, template_vars=document)
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


def get_templates_in_dir(template_dir, glob_patterns=('*.twig',)):

    files = [fn for pat in glob_patterns for fn in sorted(glob.iglob(os.path.join(template_dir, pat)))]
    print(f"\nTemplate files in {template_dir!r}:", file=sys.stderr)
    print("\n".join(f" - {fn!r}" for fn in files), file=sys.stderr)

    templates_by_name = {os.path.splitext(os.path.basename(fn))[0]: fn for fn in files}
    templates_by_name.update({fn: fn for fn in files})
    pprint(templates_by_name)

    return templates_by_name