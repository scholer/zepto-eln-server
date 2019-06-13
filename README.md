# Zepto ELN/Notebook server


Basic web server app for serving Markdown documents as HTML-compiled web pages, written in Python.
Inspired by Pico CMS. For local and online document browsing and rendering.

A flat-file, Markdown-based, wiki-style notebook web app viewer, 
specialized for viewing electronic laboratory notebooks and journals (ELNs).


This is a Python equivalent to my NextPicoELN nextcloud app/plugin.
I created this because I wanted to view Markdown documents locally on my computer,
without setting up a Nextcloud server and install my NextPicoELN nextcloud app.



## Purpose and design goals:

There are a lot of Markdown-based flat-file content-management systems and similar out there, 
including Pico, Grav, and many more. 
They are all really fine for what they aim to do. 
I just need a Markdown web viewer that does something different.

This web app was created for two main purposes:

**First**, to provide a *portable* Markdown viewer, 
using standard no-magic Markdown files, and with the option to render standard, portable HTML.

* What the former means is that the Markdown files shouldn't need to use special variables to reference image files.
In Pico, for instance, images are all placed in a special "static" folder, 
and to insert images on the Markdown page, one must use the special Pico %variable% placeholders, 
to reference the image, like so: `![Image Title](%base_url%/assets/image.png)` 
(From the [Pico docs](http://picocms.org/docs/#creating-content).)
However, for my application, I need to be able to reference images that are located next to the markdown document, 
in the same folder. I.e. I need to be able to be able to insert an image using  
`![My image](image.png)`, and it should show the `image.png` file situated next to the markdown file.

* What the latter means, is that the HTML generated by the app should portable HTML, specifically portable links.
What this means is that, using the example above, when I insert an image with `![My image](image.png)`, 
the href URI generated in the HTML should be relative to the page, not an absolute URI.
This way, the HTML can be saved to a file next to the markdown document and the image file,
opened locally, on any computer, and it should look "right".

This is very similar to how many "static website" generators work, 
but unfortunately none of the "online CMS" systems work this way.



## Getting started


As always, it is recommended to install python apps using a dedicated environment for that application.
That way, you won't have to worry about version conflict during upgrades.
There are several programs for creating Python environments: `conda`, `pipenv`, `virtualenv`, and the built-in `venv`.
Each tool has a different aim and focus. 
The built-in `venv` (and the predecessor `virtualenv`) are the most basic, 
while `pipenv` is a more unified tool focused on making "reproducible environments".
Finally, `conda` is focused more on being a multi-purpose "package manager",
and can be used to manage environments and installing packages not just for Python, 
but also for e.g. Scala, R and Julia.
I personally use `conda`, but you can use whichever you prefer.

To create a new environment with `conda`, use the following command in your terminal: 
`conda create -n zepto-eln python=3 flask jinja pyyaml markdown click`.

Then activate your environment using: 

* `activate zepto-eln` (Windows command prompt).
* `source activate zepto-eln` (Windows PowerShell, OSX, or Linux).


Then download and install ZeptoELN, either the stable release version, or the latest development version 
(make sure you are still in the `zepto-eln` environment):

* `pip install zepto-eln` 
    (to get stable release)
* `git clone https://github.com/scholer/zepto-eln-server.git && cd zepto-eln-server && pip install -e .` 
    (to install development version).

Prepare and configure the Zepto ELN flask web app (use `export` instead of `set` if you are on OSX or Linux):

```text
set FLASK_ENV=development
set ZEPTO_ELN_DOCUMENT_ROOT=D:/path/to/your/documents
set ZEPTO_ELN_TEMPLATE_DIR=D:/path/to/your/documents/templates
```

Then run the Zepto ELN web app
(make sure you are still in the `zepto-eln` environment):
```cmd
set FLASK_APP=zepto_eln.eln_server.eln_server_app
flask run
```


For more info on running and configuring Flask apps, see:

* http://flask.pocoo.org/docs/dev/cli/  - for how to run a Flask app.
* https://github.com/theskumar/python-dotenv - for how to use `.env` files.
* http://flask.pocoo.org/docs/dev/quickstart/ - Quick Start introduction to Flask.


## Basic usage:


1. Select a folder where you keep all your Markdown documents and other things 
    that you might need to include in your documents, e.g. images, scripts, etc.
    You can create sub-folders inside your main "document root" folder.
    
2. Create Markdown documents using e.g. a text editor.
    Markdown documents are just plain text files ending with `.md` instead of `.txt`.
    Write and edit your Markdown documents using standard Markdown syntax.
    
3. Run Zepto ELN Server, as outlined in the section above.

4. Go to `http://localhost:5000/` (or whatever port you have configured your app to run on),
    and view your Markdown documents.
    






## What this app is not intended for:


1. Zepto ELN/Notebook server is not intended for *editing* Markdown documents.
    * If you need to edit local Markdown files, simply use a proper text editor.
        I personally edit all my Markdown documents using Sublime Text, 
        with the "Markdown Extended" and "Markdown Preview" packages installed.
    * If you want to edit Markdown documents *"in the cloud"*, 
        then either use a third-party markdown file editor with support for your cloud,
        or use whatever apps your cloud provides for editing text/markdown files.
        For instance, there is a whole bunch of Android and iOS apps that can be used to edit 
        Dropbox text files, including Markdown documents.
        Dropbox and NextCloud also provide web apps that you can use to edit text/markdown files
        directly in the browser.

2. Zepto ELN/Notebook server is not intended for *revision control* of Markdown documents.
    * If you just need to keep track of files on your local computer, use *`git`*, 
        which is the perfect tool for revision control of local text files.
    * If you keep your files "in the cloud", your cloud should provide the revision control you need. 
    * It is also perfectly possible to use git with files in your Dropbox/NextCloud folder;
        just make sure to place the Git "repository" outside of your Dropbox/NextCloud folder,
        e.g. using the `--separate-git-dir` command line argument.
        (Keeping a Git repository inside a dropbox folder is likely to eventually corrupt the Git repository.)  
        
3. Zepto ELN/Notebook server is not intended as a *publicly facing web server*.
    * I created Zepto ELN to run locally (or behind basic web authentication through a server program),
        as a basic Markdown viewer;
        I did not create it to be a highly performant, super-secure web server.
    * If you need to serve Markdown files to the public, use an app that is created with that design goal,
        either a *CMS*, a *Wiki*, or a simple *static site generator*. See below for suggestions.




## FAQs

> Q: What's in the name "Zepto ELN"?

A1: The "Zepto" part is just a derivatization of "Pico".
I started this project after creating a fork (called NextPicoELN) of the "CMS Pico" NextCloud app,
which again is based on the "Pico CMS" app (both written in PHP).
The NextPicoELN fork is a NextCloud app, with the same "purpose and design goals" as stated above,
i.e. serving *portable, standard* Markdown documents, 
where e.g. images are stored next to the Markdown documents, 
rather than in a separate `assets/images` folder.

A2: The "ELN" part is an abbreviation of "Electronic Laboratory Notebook". 
This is just to indicate that the web app is designed mostly to be useful in a laboratory setting,
where researchers work with experiments and projects.
You can use Zepto ELN as a regular "Markdown Notebook server", 
And indeed I have considered simply calling this "Zepto Markdown Notebook Server",
since that's what it primarily is.




## Appendix I: Prior art - Other flat-file Markdown-based web apps:


### Markdown-based static site generators:

Static website generators work by generating/compiling HTML files locally, 
    using the Markdown files as input.
    The generated HTML files can be browsed and viewed locally, or uploaded to a web server.


* Jekyll - written in Ruby.
* Hexo - written in Javascript/Node.js.
* [GitBook](https://github.com/GitbookIO/gitbook) - written in Javascript, 
    specializing in writing technical documentation.
* [Hugo](https://gohugo.io/) - Popular and active static site generator, written in Go.
* Gatsby 
* NUXT
* MkDocs - created as an alternative to Sphinx for compiling Python documentation documents. 
    Written in Python (of course).
* [Pelican](https://github.com/getpelican/pelican) - Markdown and reST documents with Jinja templating. 
    Written in Python.
* MetalSmith
* Middleman
* Spike
* Octopress
* Brunch
* Next
* VuePress


> Q: Why Zepto ELN/Notebook server is different from static site generators:

* Zepto ELN/Notebook server compiles Markdown documents as-needed, on the fly.
    With static site generators, a typical, simple workflow is 
    (1) create/edit markdown documents, (2) compile all Markdown files to HTML,
    (3) upload the files to your server, or view them locally.
    With Zepto ELN/Notebook server, the "compilation" step happens automatically,
    so all you have to do is the "create/edit documents" 
    and the "view the documents" parts.



### Flat-file CMS:

Content Management System (CMS) is actually a very generic term used to describe applications 
that manage files and documents (content), i.e. provides mechanisms for uploading or editing the content,
and control who has access to the content.

A very popular category of CMS application is basic web publishing systems,
used to author and publish anything from simple web pages and blogs, 
up to full-scale web sites.

CMS apps are often classified by how they store documents and other content.
A "flat-file CMS" simply means that the documents and all other files are stored as actual files on the disk. 
This is different from CMS apps that stores all documents in e.g. a database.


**Markdown-based flat-file CMS:**

* Pico
* Grav


**Other, non-markdown, flat-file CMS apps:**

* Get Simple CMS - PHP,  
* Baun CMS - PHP, Twig templates, last update 2016.
* Urubu - Python, using python-builtin http server, last update 2018.


> Q: Why is Zepto ELN/Notebook server different from flat-file CMS apps?

* Flat-file CMS apps are generally designed to be highly performant in order to serve the website documents 
    to a large number of users, and provide ways to control what content is available to the public. 
    This obviously sounds attractive, but it generally comes with some 
    design decisions that I wanted to avoid. 
    * For example, the popular Pico CMS has images and scripts in a dedicated `assets` folder, 
        which lives in a separate folder outside the Markdown documents, 
        and is referenced using the special `%base_url%` Pico variable, as in `%base_url%/assets`.
        On the other hand, I really need documents, images, and other related files,
        to be located within the same local folder. 
        I also wanted my Markdown files to use standard Markdown syntax, that can be compiled and (pre-)viewed everywhere, 
        and not have my markdown documents littered with system-specific variables.
    * Another popular CMS, Grav CMS, just has a really weird requirement for what pages are visible,
        e.g. pages needs to be prefixed by a two-digit number in order to be visible.
    * Again, these CMS apps each have their reasons for doing it this way. 
        It just isn't compatible with how I want to create, browse, and view my Markdown documents.


### Flat-file wiki software:

Wiki apps are different from CMS apps in their focus.
Wiki apps focus on *collaborative document/page authoring* and document revisioning.
The most well-known wiki-based website is, of course, [Wikipedia](https://wikipedia.org),
which runs on the [Mediawiki](https://mediawiki.org) wiki application.
However, there are many more wiki applications, each with its own set of features and design goals.
Some wiki software is designed to run very large websites, such as Wikipedia.
Other wiki software is intended more for creating personal notebooks.

Since the documents can be edited by a lot of people, sometimes even anonymously, 
it is important to be able to revert changes that aren't good.
Hence, almost all wiki software provides a built-in way to keep track of changes and 
compare different versions of a page.

Again, the "flat-file" moniker refers to how documents are stored.



**Markdown-based flat-file wiki software:**

* MDwiki
* Wiki.js
* Miki
* Gollum
* Realms
* ittywiki (2014)
* Precious - Python, based on Bottle, last update 2013.

**Other non-Markdown flat-file wiki software:**



**Other wiki software (not flat-file):**

* TiddlyWiki classic 
* TiddlyWiki5 - Javascript/Node.js 



> Q: Why is Zepto ELN/Notebook server different from flat-file Wiki apps?

* Wiki apps are generally designed to handle all of the following:
    (1) Creating, editing, and reorganizing documents,
    (2) Tracking document revisions, and
    (3) Viewing documents.
* I use other tools for the first two points - 
    a text editor for editing documents, a file browser for re-organizing documents,
    and Git for tracking document revisions.
* Thus, my workflow generally does not play well together with most wiki applications.



### Other interesting projects;

* [Intelligent Document Environment](https://github.com/documize/community).





### List and overviews:
 
Overviews of flat-file CMS and wiki:

* https://github.com/ahadb/flat-file-cms
* https://github.com/postlight/awesome-cms
* https://github.com/gothburz/awesome-cms
* https://github.com/n370/awesome-headless-cms

Overviews of Markdown-related projects:

* https://github.com/mundimark/awesome-markdown


Overview of static site generators:

* https://github.com/myles/awesome-static-generators
* https://www.staticgen.com/
* https://www.netlify.com/blog/2017/05/25/top-ten-static-site-generators-of-2017/





