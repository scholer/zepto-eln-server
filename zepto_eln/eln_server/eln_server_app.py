# Copyright 2018, Rasmus S. Sorensen, rasmusscholer@gmail.com


r"""



# On Windows we use `set` instead of `export`:
set FLASK_ENV=development
set FLASK_APP=eln_server_app.py
set ZEPTO_ELN_DOCUMENT_ROOT="C:\Users\rasse\Dropbox\_experiment_data"
set ZEPTO_ELN_DOCUMENT_ROOT="D:/Dropbox/_experiment_data/"
set ZEPTO_ELN_DOCUMENT_ROOT=D:/Dropbox/_experiment_data
flask run

You can also use a `wsgi.py` file to configure Flask.

"""

import os
from pprint import pprint
import yaml
from flask import Flask, send_from_directory, redirect, abort

from zepto_eln.md_utils.markdown_compilation import compile_markdown_document

from .path_utils import expand_abbreviated_path
from .path_utils import get_page_tree_recursive
from . import default_settings

# TODO: Use the flask built-in config object for all configuration-related things.
# TODO: https://flask.palletsprojects.com/en/1.1.x/config
try:
    CWD_CONFIG = yaml.safe_load(open('.zepto-eln-server.yaml'))
except FileNotFoundError:
    CWD_CONFIG = {}

TEMPLATE_DIR = os.environ.get('ZEPTO_ELN_TEMPLATE_DIR')
if TEMPLATE_DIR:
    TEMPLATE_DIR = TEMPLATE_DIR.strip('"')  # In case we have accidentally quoted the dir too much.
    # TEMPLATE_DIR = os.path.abspath(TEMPLATE_DIR)  # Make it absolute?
print("TEMPLATE_DIR:", repr(TEMPLATE_DIR))

# The include_dirs patterns are matched against the full path relative to document_root.
# E.g. "2018*" will match "2018_Aarhus/" and all sub-directories.
# This is currently only used as a page-tree filter; doesn't restrict what files may be served.
# Maybe rename environment variable to ZEPTO_ELN_PAGETREE_INCLUDE_DIRS ?
PAGETREE_INCLUDE_DIRS = os.environ.get('ZEPTO_ELN_PAGETREE_INCLUDE_DIRS')
if PAGETREE_INCLUDE_DIRS:
    PAGETREE_INCLUDE_DIRS = PAGETREE_INCLUDE_DIRS.split(';')
else:
    # True = include all dirs; False or None = do not include dirs.
    PAGETREE_INCLUDE_DIRS = CWD_CONFIG.get('pagetree_include_dirs', True)
print("PAGETREE_INCLUDE_DIRS:", repr(PAGETREE_INCLUDE_DIRS))

SERVE_CACHED_HTML_IF_NEWER = True

app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.config.update(
    EXPLAIN_TEMPLATE_LOADING=True,
)
app.config.from_object(default_settings)
try:
    app.config.from_envvar('ZEPTO_ELN_SERVER_SETTINGS')
except RuntimeError:
    pass

homepage_txt = """
HOME PAGE
<br/><br/>
#TODO: Still need to provide a usable front-page (incl. template). 

(You can browse to an individual markdown file to see the pagetree.)
"""

# TODO: There is a but where http://127.0.0.1:5000/2019_Aarhus returns a runtime error because no index file was found,
# TODO: but http://127.0.0.1:5000/2019_Aarhus/ returns http://127.0.0.1:5000/2019_Aarhus/RS-Experiments-overview.md
# It might be due to how the path is generated, @app.route('/<path:path>') - if



@app.route('/')
def index():
    print(f"\n\nServing @app.route('/')")
    return homepage_txt


@app.route('/<path:path>')  # path: is a type specifier, allowing the rest to contain slashes.
def serve_file(path, serve_html_file_if_newer=SERVE_CACHED_HTML_IF_NEWER, update_html_file=True):
    """

    Args:
        path:

    Returns:
        If a string is returned, that string is, by default, placed inside the <body> of a HTML document,
        and the HTML document is sent to the client.

        If you don't want to embed the content inside a HTML document, you need to return a custom request
        or otherwise create a non-string response.
    """
    print(f"\n\nBEGIN serve_file() - path={path}")
    try:
        document_root = os.environ['ZEPTO_ELN_DOCUMENT_ROOT']
    except KeyError:
        document_root = os.getcwd()
        print("ZEPTO_ELN_DOCUMENT_ROOT environment variable not set; using current directory:", document_root)
    document_root = os.path.abspath(document_root)
    print("document_root:", document_root)
    fs_path = os.path.join(document_root, path)

    print(" - Path:", path)
    # print(" - os.path.realpath(path):", os.path.realpath(path))
    # print(" - os.path.abspath(path):", os.path.abspath(path))
    print(" - Abspath:", fs_path)

    assert fs_path.startswith(document_root)

    if os.path.isfile(fs_path):
        print("Sending directly-requested file:", fs_path)
        return send_from_directory(document_root, path)
    # md_filepath = fs_path + '.md'
    if os.path.isfile(fs_path + '.md'):
        # Request for showing compiled markdown document:
        print("Requested HTML-compiled markdown document:", fs_path)
        html_filename = fs_path+'.html'
        print(f"Does {html_filename} exist:", os.path.isfile(fs_path+'.html'))
        if (serve_html_file_if_newer and os.path.isfile(fs_path+'.html')
                and os.path.getmtime(fs_path+'.html') > os.path.getmtime(fs_path+'.md')):
            print("Sending cached .html document:", fs_path+'.html')
            # return send_from_directory(document_root, fs_path+'.html')
            html_file = fs_path+'.html'
            return open(html_file).read()
        else:
            # Generate page tree:
            # not just pages, also folders. Maybe "navigation tree" or "sitemap" ?
            navigation_tree = get_page_tree_recursive(
                document_root, rel_root=document_root, depth=4, include_files=["*.md"], include_dirs=PAGETREE_INCLUDE_DIRS,
            )
            # We just get a dict for the top/root element, but we actually just want the children:
            navigation_tree = navigation_tree['children']  # or [navigation_tree] if you want a collapsible root
            print("navigation_tree:")
            pprint(navigation_tree)
            template_vars = {
                'navigation_tree': navigation_tree,
                'request_path': '/' + path,
                'documents_root_url': '/',  # aka `base_url` in e.g. pico?
            }
            # Compile markdown document:
            print("Compiling Markdown file:", fs_path+'.md')
            # TODO: Do templating using Flasks Jinja system, which adds nice variables, e.g. request.url.
            document = compile_markdown_document(
                path=fs_path+'.md',
                outputfn='{filepath_noext}.html' if update_html_file else False,
                yfm_parsing=True, yfm_errors='warn',  # Try to parse YFM, but only print warning if it fails.
                template_dir=TEMPLATE_DIR,
                template_vars=template_vars,
            )
            print(f"Serving {fs_path} as freshly-compiled HTML ({len(document['html'])} characters)")
            return document['html']
    else:
        # Try to see if we have an abbreviated path:
        print(f" - Path {path!r} is not a file, and neither is {path+'.md'!r}.")
        print(f" - Checking if path {path!r} is an abbreviated path...")
        try:
            # Should we do this relatively to the current path-dir, or absolute versus document_root?
            expanded_path = expand_abbreviated_path(
                path, root=document_root,
                return_index_for_dir=True, strip_indexfile_ext=True,
                return_relpath=True, ensure_forwardslash=True)
        except RuntimeError as exc:
            print(f"ERROR, {path!r} could not be expanded: {exc}")
            return abort(404, description=str(exc))
        else:
            expanded_path = '/' + expanded_path  # Make the redirect absolute (i.e. relative to document_root).
            print(f" - path abbreviation expansion found, redirecting to:", expanded_path)
            return redirect(expanded_path)


    return f'<p>SOMETHING WENT WRONG!</p><p>{path}</p><p>{fs_path}</p><p>'



def cli():
    # This works for simple, local usage, but is not recommended for production development,
    # since a lot of things are not equivalent to running the app with an application server.
    # It also doesn't work well for development because reloads may not work properly.
    # In conclusion: Just use the `flask` program (or application server) to run the flask app.
    app.run(host='0.0.0.0', port=8000)


if __name__ == '__main__':
    cli()