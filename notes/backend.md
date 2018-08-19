

Backend web frameworks:
========================

The backend web frameworks is responsible for producing the content, 
taking user requests and other input, retrieving content from storage,
and producing a suitable request for the user.


Python web frameworks, overview:
--------------------------------


Micro-frameworks:
* Flask - “a microframework for Python based on Werkzeug, Jinja 2 and good intentions.”
    Uses "blueprints"
    Has its own web server, although this isn't recommended for production (use
* Bottles - Microframework with focus on simplicity, originally for making APIs. Single file with no dependencies.
* Falcon - Fast WSGI framework,
    http://falconframework.org/, https://falcon.readthedocs.io/en/stable/
    Requires a WSGI web server to run, e.g. gunicorn or uWSGI
* CherryPy - Used by TurboGears.
* Hug

Asynchronous frameworks:
* Quart - a Flask-inspired ASGI microframework using asyncio.
    Adds the following to Flask: Websockets, HTTP/1.1 request streaming, HTTP/2 server push.
    Recommends hypercorn as web server because not all ASGI servers support the extra features.
    https://gitlab.com/pgjones/quart
* Sanic - built on uvloop.
* Tornado - the "original standard library web server and framework".


Full-stack frameworks:
* Django
* Pyramid - "Pyramid is intended for bigger and more complex applications than Flask."
* TurboGears
* web2py - Web2py does not support Python 3.
* reahl


Question:
* Q: Do I need to make a full "web app", or just serving up simple documents?
  A: I just need to serve simple documents.
  C: I should pick a micro-framework, e.g. Flask, Falcon, or Pyramid. A full-stack framework, e.g. Django is overkill.


Note:
* Django, TurboGears, and more are so-called "full-stack" frameworks, which means they provide not only web server,
    but also templating, persistence, storage, and database connections,

Refs:
* https://wiki.python.org/moin/WebFrameworks
* http://docs.python-guide.org/en/latest/scenarios/web/
* https://www.airpair.com/python/posts/django-flask-pyramid
* https://hackernoon.com/top-10-python-web-frameworks-to-learn-in-2018-b2ebab969d1a
* https://www.slant.co/versus/1398/1744/~flask_vs_falcon




Python web framworks, comparison:
----------------------------------



### Flask

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
```

Save above to `hello.py`, then run: `FLASK_APP=hello.py flask run`.


### Falcon:

```python
import falcon

# Falcon follows the REST architectural style, meaning (among other things) that you think 
# in terms of resources and state transitions, which map to HTTP verbs.
class ThingsResource(object):
    def on_get(self, req, resp):
        """ Handles GET requests. """
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = 'Two things awe me most, the starry sky above me and the moral law within me.\n\n ~ Immanuel Kant'

app = falcon.API()  # falcon.API instances are callable WSGI apps
things = ThingsResource()  # Resources are represented by long-lived class instances
app.add_route('/things', things)  # things will handle all requests to the '/things' URL path
```

Save file to `things.py` and run with e.g. gunicorn or other WSGI application server:
`$ gunicorn things:app`, or 
`$ waitress-serve --port=8000 things:app`



### Sanic:

```python
from sanic import Sanic
from sanic.response import json

app = Sanic()

@app.route('/')
async def test(request):
    return json({'hello': 'world'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```


Web servers:
------------

The web server is responsible providing the infrastructure through which the web client and the 
backend web framework communicate, relaying requests from the user to the server, 
and transmitting the response to the user.

Being open to the public, a web server's focus is often on performance, security, and configurability.


Dedicated web servers:
* Nginx
* Apache, with mod_wsgi


Python-based web application servers (most can serve as stand alone web servers in a development environment):
* Chaussette
* CherryPy - used by TurboGears, web2py.
* Gunicorn
* Rocket
* Spawning
* Tornado
* twisted.net
* Waitress
* uWSGI - https://github.com/unbit/uwsgi/ - Written in C

Note:
* On Windows where Gunicorn and uWSGI don’t work yet you can use Waitress server.


Refs:
* https://docs.python.org/3.4/howto/webservers.html
* https://wiki.python.org/moin/WebServers





Serving static files:
----------------------

Static files, middleware:
* dj-static - simple Django middleware, serve static assets with a WSGI server like Gunicorn.
    https://github.com/heroku-python/dj-static
* static
    https://pypi.org/project/static/
* WhiteNoise - "Radically simplified static file serving for Python web apps."
    http://whitenoise.evans.io/en/stable/ - a WSGI middleware to serve static files.


Nginx:
* When serving static files with Nginx, you may want to consider setting the following to prevent caching:
    expires off;
    sendfile  off;
    c.f. https://serverfault.com/questions/269420/disable-caching-when-serving-static-files-with-nginx-for-development


Refs:
* https://medium.com/@jgefroh/a-guide-to-using-nginx-for-static-websites-d96a9d034940
* https://docs.nginx.com/nginx/admin-guide/web-server/serving-static-content/


Discussion: Serving frequently-changing static files:
* Static files are good if they can be cached when served.
* If we need to do multiple `stat` calls to check file modification time, then there may not be that much to gain from
    "caching" the compiled HTML to file.
* However, if the compilation is done "properly" and doesn't introduce any server-specific stuff in the HTML,
    i.e. doesn't change links/URIs, then it may be nice to save the compilation anyways, so it can be accessed locally.
* In any case, this is all intended to be served locally, so don't worry about performance.


Backend setups:
---------------

* Many frameworks have a built-in pure-python web server.
* However, it is recommended to use a dedicated web server for production.
* Some web servers, like uwsgi and gunicorn, can run your web app directly.
* Other web servers, like Nginx, needs a WSGI driver to deliver the content.

So, you have the following options:
* Flask, using its built-in server (for development).
* Flask, run through gunicorn or uWSGI (application servers).
* FLash, run through gunicorn or uwsgi interfacing to nginx (with nginx serving pages to the outside).

Obs:
* WSGI and uwsgi are protocols, defining how a web app can interface with a web server, like Nginx or Cherokee.
* uWSGI is a WSGI/uwsgi application server program that implements uwsgi.
* WSGI =  Web Server Gateway Interface.
    There are other web app-server interface protocols, e.g. PSGI (Perl), CGI, FastCGI,
* These protocols just specify how a web server should forward requests to an application server,
    and how the application server should respond.
* Between the application and server you can also insert middleware,
    e.g. load balancers, login/auth handlers, etc.
* Many application servers can be configured to use HTTP as their protocol.
    This effectively makes them http web servers.
    However, that does not mean they are neither fast, secure, or stable web servers.
    The application servers are created to take a request and produce a response as fast as possible,
    running one or more instances of the web app.

Regarding web app/framework vs application server vs web server:
* Confluence is a web app.
* Tomcat is an application server, which runs Confluence web app.
* Apache is the web server, which serves the content produced by Confluence via Tomcat.


Refs:
* http://flask.pocoo.org/docs/1.0/deploying/uwsgi/
* https://stackoverflow.com/questions/7739810/wsgi-vs-uwsgi-with-nginx
* https://serverfault.com/questions/590819/why-do-i-need-nginx-when-i-have-uwsgi


Checking responses:
-------------------

Curl is the "golden standard", but you may also want to try something more modern, e.g. HTTPie:

```commandline
pip install httpie
http localhost:8000
```


Conclusion:
-----------

* I don't need a full-stack web framework; Flask or Falcon should do the trick.



Templating systems:
====================

See [templating.md](templating.md).



