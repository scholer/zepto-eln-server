
Packaging:
==========


Packaging, distribution, and namespaces:
----------------------------------------

It is perfectly possible to have multiple distribution using a shared namespace (since Python 3.3).

* https://packaging.python.org/guides/packaging-namespace-packages/#native-namespace-packages

All you have to do is to create the outer "namespace package" without a `__init__.py` file:

```text
setup.py
mynamespace/
    # No __init__.py here.
    subpackage_a/
        # Sub-packages have __init__.py.
        __init__.py
        module.py
```

In my case, using a shared `zepto_eln` namespace, this looks something like:

```text
# In package 1:
setup.py
zepto_eln/
    # No __init__.py here.
    subpackage_a/
        # Sub-packages have __init__.py.
        __init__.py
        module.py


# In package 2:
setup.py
zepto_eln/
    # No __init__.py here.
    subpackage_a/
        # Sub-packages have __init__.py.
        __init__.py
        module.py


```



