# Python Method Cache

[![Build Status](https://travis-ci.org/eieste/MethodCache.svg?branch=master)](https://travis-ci.org/eieste/MethodCache)
[![PyPI version](https://badge.fury.io/py/method-cache.svg)](https://badge.fury.io/py/method-cache)
[![Documentation Status](https://readthedocs.org/projects/methodcache/badge/?version=latest)](https://methodcache.readthedocs.io/en/latest/?badge=latest)

## What it does

MethodCache can be used to cache the result of an method in a flexible way.
This libary has no dependencies!

**Currently only TTL Cache available**

The cache storage can be segmented in categories.
Methods with the ``@cache`` decorator are saved in these categories.

## Example
```python
from methodcache import cache, Store
import time

# TTL in Seconds (Default TTl is 60)
st = Store(ttl=60*300)

# Define Store for this Cache, and overwrite Store TTL. And categorize this cache object to demo
@cache(store=st, ttl=5, category="demo")
def doothings(a,b,c):
    # Do here what ever you want.
    # eg. MySQL querys or other slow operations
    time.sleep(2)
    return a+b+c

# Slow Execution
doothings(1,2,3)
# Slow Execution

doothings(4,5,6)

# Fast Execution because the Cache was used
doothings(1,2,3)
time.sleep(2)

# Slow Execution because the Cache TTL is Expired
doothings(1,2,3)

```

## Documentation

[Read the Docs](https://methodcache.readthedocs.io/en/latest/)

or 
show ``example.py``
