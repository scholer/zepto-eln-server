# Copyright 2018, Rasmus S. Sorensen, rasmusscholer@gmail.com

"""

Basic web server app for serving Markdown documents as HTML-compiled web pages.

This is a Python equivalent to my NextPicoELN nextcloud app,
which you can run locally without setting up a nextcloud server and install the NextPicoELN app.


The functionality is very simple:
* The server is started within a directory and will serve files within that directory.
* If the client is requesting an actual file within the directory, that file is served unmodified.
    Note: If running this server behind Nginx or similar, configure Nginx directly to
    check for static files (using the `try_files`) directive.
    Although for html files, this check should compare the .html file's modification date with any .md file,
    in case we want to re-compile the HTML file from the markdown source.
* If the client is requesting a file that doesn't exists, the server checks if the request with
    '.md' matches an actual Markdown file, and if the request with '.html' matches an actual HTML file.
    * If the HTML file is newer (based on modification date), the HTML file is served.
    * Otherwise, the Markdown document is compiled, templated, and saved with '.html',
        updating any existing HTML file in the process,
        and the HTML-compiled document is then served.

* The `/eln_server/` entry point accepts "abbreviated" paths which will be expanded:
    That is, if you request `/eln_server/2018/RS532/`
    and `<root>/2018` doesn't exists, but `<root>/2018_Aarhus` does exists,
    then the request is redirected to `/eln_server/2018_Aarhus/RS532/`.
    If `<root>/2018_Aarhus/RS532/` doesn't exists, but `<root>/2018_Aarhus/RS532_Test_experiment/` does,
    then the request is redirected to `/eln_server/2018_Aarhus/RS532_Test_experiment/`.
    If `<root>/2018_Aarhus/RS532_Test_experiment/` exists and is a folder,
    then if index.md exists, then we redirect to `/eln_server/2018_Aarhus/RS532_Test_experiment/index`
    otherwise, the first .md file that is fully included in the folder name is served by redirecting to
    that filename (without extension).
    For instance, say we have the following files:
        README.md, RS532.md, RS532.html, analyze_RS532.py, RS532a.md, RS.md, RS532.bak.md.
    First we filter .md files:
        README.md, RS532.md, RS532a.md, RS.md, RS532.bak.md.
    Then we remove files that doesn't start with the same as the directory:
        >>> files = [fn for fn in files if dirname.startswith(os.path.splitext(fn)[0])]
        RS532.md, RS.md
    Then we take the last file:
        >>> fn = sorted(files)[-1]
        RS532.md
    Then we redirect to:
        `/eln_server/2018_Aarhus/RS532_Test_experiment/RS532`.

* Note:
    If requesting absolute URIs, and the URI doesn't start with `/eln_server`
    (or one of the other recognized entry points), then the server will automatically
    redirect the request to `/eln_server/{uri}`.

* The app has an option to save the compiled HTML from `file.md` to `file.html`,
    (if

* We may also support various metadata directives, e.g.:
    `/eln_server/expid:RS532
    This will serve the last indexed markdown file with `expid: RS532` metadata entry.
    This requires keeping a persistent index and indexing files either when they are changed,
    or running the indexing as-needed, or re-indexing the files periodically.


Alternative names:

* PicoELN
* Pipto ELN
* Pipto Markdown Notebook
* (Pipto = "to fall down, from a higher to a lower position")


"""