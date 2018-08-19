

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


Templating systems, comparison:
* Jinja2 - the ubiquitous `{{` template logic annotations.
* Chameleon - uses embedded `tal:` html tag attributes.
* Mako  - uses `<%` to add templating logic
*



Refs:
* http://vschart.com/list/template-language/
* http://jinja.pocoo.org/docs/2.10/switching/
* https://en.wikipedia.org/wiki/Comparison_of_web_template_engines
* https://www.quora.com/Was-Twigs-syntax-inspired-by-Liquid


What frameworks and servers have a ready-to-amend Docker image?

* https://hub.docker.com/
* https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask/
* https://hub.docker.com/r/p0bailey/docker-flask/ - also with uwsgi and Nginx.
* https://hub.docker.com/r/danriti/nginx-gunicorn-flask/




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

