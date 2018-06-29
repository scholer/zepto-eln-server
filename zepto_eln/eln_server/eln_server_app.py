# Copyright 2018, Rasmus S. Sorensen, rasmusscholer@gmail.com


r"""



# On Windows we use `set` instead of `export`:
set FLASK_ENV=development
set FLASK_APP=eln_server_app.py
set ELN_SERVER_DOCUMENTS_ROOT="C:\Users\rasse\Dropbox\_experiment_data"
set ELN_SERVER_DOCUMENTS_ROOT="D:/Dropbox/_experiment_data/"
flask run

You can also use a `wsgi.py` file to configure Flask.

"""

import os
import sys

from flask import Flask, request, send_file, send_from_directory, redirect, url_for, abort, config


from .path_utils import expand_abbreviated_path
from zepto_eln.md_utils.markdown_compilation import compile_markdown_document
from . import default_settings


TEMPLATE_DIR = os.environ.get('ZEPTO_ELN_TEMPLATE_DIR')
if TEMPLATE_DIR:
    TEMPLATE_DIR = TEMPLATE_DIR.strip('"')
print("TEMPLATE_DIR:", repr(TEMPLATE_DIR))


app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.config.update(
    EXPLAIN_TEMPLATE_LOADING=True,
)
app.config.from_object(default_settings)
try:
    app.config.from_envvar('ZEPTO_ELN_SERVER_SETTINGS')
except RuntimeError:
    pass


@app.route('/')
def index():
    return 'HOME PAGE'


@app.route('/<path:path>')  # path: is a type specifier, allowing the rest to contain slashes.
def serve_file(path, serve_html_file_if_newer=True, update_html_file=True):
    """

    Args:
        path:

    Returns:
        If a string is returned, that string is, by default, placed inside the <body> of a HTML document,
        and the HTML document is sent to the client.

        If you don't want to embed the content inside a HTML document, you need to return a custom request
        or otherwise create a non-string response.
    """
    try:
        document_root = os.environ['ELN_SERVER_DOCUMENTS_ROOT']
    except KeyError:
        document_root = r"D:/Dropbox/_experiment_data/"
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
        if (serve_html_file_if_newer and os.path.isfile(fs_path+'.html') and False
                and os.path.getmtime(fs_path+'.html') > os.path.getmtime(fs_path+'.md')):
            print("Sending cached .html document:", fs_path+'.html')
            # return send_from_directory(document_root, fs_path+'.html')
            html_file = fs_path+'.html'
            return open(html_file).read()
        else:
            # Compile markdown document:
            print("Compiling Markdown file:", fs_path+'.md')
            document = compile_markdown_document(
                path=fs_path+'.md',
                outputfn='{filepath_noext}.html' if update_html_file else False,
                template_dir=TEMPLATE_DIR,
            )
            print(f"Serving {fs_path} as compiled HTML ({len(document['html'])} characters)")
            return document['html']
    else:
        # Try to see if we have an abbreviated path:
        try:
            print(f"Checking if path {path!r} is an abbreviated path...")
            expanded_path = expand_abbreviated_path(
                path, root=document_root, return_index_for_dir=True, strip_indexfile_ext=True,
                return_relpath=True, ensure_forwardslash=True)
            print(f" - path abbreviation expansion found, redirecting to:", expanded_path)
            return redirect(expanded_path)
        except RuntimeError as exc:
            print(f"ERROR, {path!r} could not be expanded:", repr(exc))
            return abort(404)  # , message=repr(exc))

    return f'<p>SOMETHING WENT WRONG!</p><p>{path}</p><p>{fs_path}</p><p>'


if __name__ == '__main__':
    # This works for simple, local usage, but is not recommended for production development,
    # since a lot of things are not equivalent to running the app with an application server.
    # It also doesn't work well for development because reloads may not work properly.
    # In conclusion: Just use the `flask` program (or application server) to run the flask app.
    app.run(host='0.0.0.0', port=8000)
