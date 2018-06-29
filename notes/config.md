

Configuration:
==============


I'm getting a little tired of re-inventing a configuration system for every project that I make.

Maybe I should look into adopting a "standard" config package?


How does Flask do configuration?
* http://flask.pocoo.org/docs/1.0/config/

```python
from flask import Flask
app = Flask(__name__)
app.config  # Basic config, with dict-like interface.
app.config.from_object('zepto_eln.eln_server.default_settings')  # load default_settings.py module (or class). 
app.config.from_envvar('ZEPTO_ELN_SERVER_SETTINGS')  # Load the python file specified by environment variable. 
```

Flask config files are just python files, where only the variables named in all upper case are stored in the config.
Thus, Flask config entries are always named in capital letters.


YAML-supported config packages (in active development):

* https://github.com/jbasko/configmanager
* https://github.com/kororo/conff
* https://github.com/sampsyo/confuse
* https://github.com/zerwes/hiyapyco
* yamlsettings



The README for layered-yaml-attrdict-config has a nice list of further yaml-based configs ():

* https://github.com/mk-fg/layered-yaml-attrdict-config - last update 2016
* confif - renamed to 'confuse'.
* loadconfig - 2015, INI-based.
* orderedattrdict - 2017
* layeredconfig - 2017
* reyaml - 2016
* configloader - 2015.
* yamlcfg - old, 2015.
* yamlconfig - old, 2011.
* python-yconfig - 2017.


There is also a large comparison at https://wiki.python.org/moin/ConfigParserShootout,
but most of these strictly use INI format, which I dislike. - I prefer YAML.

INI-based config parsers and managers:

* ConfigObj - http://configobj.readthedocs.io/en/latest/configobj.html
* 




