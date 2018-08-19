# Copyright 2018, Rasmus S. Sorensen, rasmusscholer@gmail.com

"""

Module for compiling markdown contents/documents.


Notes on the different Markdown parsers:
-----------------------------------------

Advantages of 'github' vs 'python-markdown' parser:
* Github adds style="max-width:100%;" attribute to all <img> image elements.
    This can be accomplished globally, using a template,
    on a page-by-page basis by adding a <style> tag at the top of the page,
    or on a image-by-image basis by inserting images with <img> tags, or using markdown `{: attribute lists}`.

These are the same, with the proper extension:
* Code blocks (incl inside lists) renders as expected, if "Fenced code" extension is enabled.

Python-Markdown extensions: https://python-markdown.github.io/extensions/
* Extra: markdown.extensions.extra
    Enable 'extra' features from [PHP Markdown](https://michelf.ca/projects/php-markdown/extra/).
    * Fenced Code: markdown.extensions.fenced_code
        Enable support for ```python\n...``` fenced code blocks.
    * Attribute list: markdown.extensions.attr_list
        Add HTML attributes to any element (header, link, image, paragraph) using trailing curly brackets:
        `{: #someid .someclass somekey='some value' }`.
    * Footnotes: markdown.extensions.footnotes
    * Tables: markdown.extensions.tables
* Sane Lists: markdown.extensions.sane_lists
* Table of Contents: markdown.extensions.toc




"""

import sys
import requests
import markdown

from .document_io import load_document
from .pico_utils import substitute_pico_variables
from .templating import apply_template_file_to_document

GITHUB_API_URL = 'https://api.github.com'


def github_markdown(markdown, verbose=None):
    """ Takes raw markdown, returns html result from GitHub api """
    endpoint = GITHUB_API_URL + "/markdown/raw"
    headers = {'content-type': 'text/plain', 'charset': 'utf-8'}
    res = requests.post(endpoint, data=markdown.encode('utf-8'), headers=headers)
    res.raise_for_status()
    return res.text


def compile_markdown_to_html(content, parser='python-markdown', extensions=None, template=None, template_type='jinja'):
    """ Convert markdown to HTML, using the specified parser/generator.

    Args:
        content: Markdown content (str) to convert HTML.
        parser: A string specifying which parser to use.
            Options include: 'github', and 'python-markdown' (default).
        extensions: A list of extensions to pass to the parser, or None for the default extensions set.

    Returns:
        HTML (string)

    Examples:
        >>> markdown_to_html("hello world!", parser='github')
        '<p>hello world</p>'

    """
    if parser is None:
        parser = 'python-markdown'
    if parser == 'python-markdown':
        if extensions is None:
            extensions = [
                'markdown.extensions.fenced_code',
                'markdown.extensions.attr_list',
                'markdown.extensions.tables',
                'markdown.extensions.sane_lists',
                # 'markdown.extensions.toc',
            ]
        print("\nExtensions:", extensions)
        html_content = markdown.markdown(content, extensions=extensions)
    elif parser in ('github', 'ghmarkdown'):
        try:
            # Try to use the `ghmarkdown` package, and fall back to a primitive github api call
            import ghmarkdown
            return ghmarkdown.html_from_markdown(content)
        except ImportError:
            html_content = github_markdown(content)
    else:
        raise ValueError(f"parser={parser!r} - value not recognized.")

    return html_content


def compile_markdown_document(
        path, outputfn="{filepath_noext}.html",
        parser='python-markdown', extensions=None,
        do_pico_substitution=True, do_apply_template=True,
        template_type='jinja2', template=None, template_dir=None, default_template_name='index',
        template_vars=None,
):
    """ Compile a single markdown file and apply template, return compiled HTML, optionally save HTML output to a file.

    Args:
        path: Filepath to the markdown file.
        outputfn: Save compiled HTML to this file. If '-', write HTML to stdout.
        parser: The Markdown parser to use to generate HTML.
        extensions: The Markdown extensions to use when compiling HTML.
        do_pico_substitution: Do Pico substitutions on the Markdown before compiling Markdown to HTML.
        do_apply_template: Apply a template (e.g. Jinja template).
        template_type: The templating system to use, e.g. 'jinja2'.
        template: The template (name or filename) to apply.
        template_dir: The directory to look for, if template is a name (rather than a file).
        default_template_name: The default template (name) to apply.

    Returns:
        HTML-compiled markdown.

    C.f. rsenv.eln.eln_md_to_html

    Returns:
        Document dict, with 'html' entry storing the compiled HTML.

    """
    document = load_document(path)  # dict with 'content', 'meta', 'filename', etc.

    if do_pico_substitution:
        # Perform %pico_variable% substitution:
        pico_vars = document.copy()
        pico_vars.update(document['fileinfo'])  # has 'dirname', 'basename', etc.
        document['content'] = substitute_pico_variables(document['content'], template_vars=pico_vars, errors='print')

    html_content = compile_markdown_to_html(document['content'], parser=parser, extensions=extensions)
    document['html_content_raw'] = html_content
    document['html_content'] = html_content
    document['html_body'] = html_content
    document['content'] = html_content

    if do_apply_template:
        # apply_template_file_to_document updates document['html']
        html = apply_template_file_to_document(
            document, template_type=template_type, template=template, template_dir=template_dir,
            default_template_name=default_template_name, template_vars=template_vars)
    else:
        html = document['html'] = html_content

    if outputfn:
        if outputfn == '-':
            sys.stdout.write(html)
        else:
            fmt_params = document['fileinfo'].copy()
            fmt_params.update(document['meta'])
            outputfn = outputfn.format(**fmt_params)
            with open(outputfn, mode='w', encoding='utf-8') as fd:
                print("Writing HTML to file:", outputfn)
                fd.write(html)

    return document


def compile_markdown_file_to_html(
        path, outputfn="{filepath_noext}.html",
        do_pico_substitution=True, do_apply_template=True,
        parser='python-markdown', extensions=None,
        template_type='jinja2', template=None, template_dir=None, default_template_name='index',
):
    """

    Args:
        See `compile_markdown_document()` above.

    Returns:
        HTML (str) - simply the document['html'] entry.

    """
    document = compile_markdown_document(
        path=path, outputfn=outputfn, do_pico_substitution=do_pico_substitution, do_apply_template=do_apply_template,
        parser=parser, extensions=extensions,
        template_type=template_type, template=template, template_dir=template_dir,
        default_template_name=default_template_name,
    )
    return document['html']
