from methodcache.store import Store
from methodcache.helper import WrapperFunction, WrapperParameters
from methodcache.exceptions import NoMethod, TTLExpired
import logging
# Decorator Args

logging.basicConfig(level=logging.DEBUG)


def cache(**options):
    """
        Decorator method for caching

        :param ttl: Time to life for this Cache Entry in Seconds
        :param store: Storage Object. To this object the cache entry was saved
        :param category: String in which Category the cache object should be sorted
    """
    if "store" not in options:
        setattr(Store.__class__, "_default_store", Store())
        store = getattr(Store.__class__, "_default_store")
    else:
        store = options["store"]
    assert isinstance(store, Store)

    if "ttl" not in options:
        ttl = options["store"].ttl
    else:
        ttl = options["ttl"]
    assert type(ttl) is int

    if "category" not in options:
        category = "default"
    else:
        category = options["category"]
    assert type(category) is str

    _store = store
    _category = category
    _ttl = ttl

    def funcwrapper(func):
        """
            Decorator Wrapper

            :param func: Orginal Funciton
            :return: Modifed Function
        """

        def methodcall(*args, **kwargs):
            """
                Cache Implementaiton Checks if method in same category with the same
                :param args:
                :param kwargs:
                :return:
            """
            _func = WrapperFunction(func)
            _params = WrapperParameters(args, kwargs)

            method_store = _store.get_method_store(*_category.split(":"))
            try:
                meth_obj = method_store.get_method(_func, _params)
                return meth_obj.get_result()
            except NoMethod as e:
                result = _func.get_func()(*args, **kwargs)
                method_store.create(_func, _params, result)
                return result
            except TTLExpired as e:
                result = _func.get_func()(*args, **kwargs)
                method_store.create(_func, _params, result)
                return result

        return methodcall

    return funcwrapper
