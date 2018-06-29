


Comparison of web framworks:
-----------------------------



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




