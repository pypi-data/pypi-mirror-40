try:
    from .__version__ import VERSION
except:               # pragma: no cover
    VERSION='unknown'

class ProxyType(object):
    pass

class ReadOnlyProxyType(ProxyType):
    def __str__(self):
        return "%s(%s)" % (type(self).__name__,str(self._t))
    def __repr__(self):
        return "%s(%s)" % (type(self).__name__,repr(self._t))

class ReadOnlyListProxy(ReadOnlyProxyType):
    def __init__(self,l):
        if not issubclass(type(l),list):
            raise TypeError("'%s' only supports lists, not '%s'." % (type(self).__name__,type(l).__name__))
        self._t = l
    def __add__(self,x):
        return self._t + x
    def __contains__(self,x):
        return x in self._t
    def __eq__(self,x):
        return self._t == x
    def __format__(self,*args,**kwargs):
        return self._t.__format__(*args,**kwargs)
    def __ge__(self,x):
        return self._t >= x
    def __getitem__(self,x):
        return self._t[x]
    def __gt__(self,x):
        return self._t > x
    def __iter__(self):
        return iter(self._t)
    def __le__(self,x):
        return self._t <= x
    def __len__(self):
        return len(self._t)
    def __lt__(self,x):
        return self._t < x
    def __mul__(self,x):
        return self._t * x
    def __ne__(self,x):
        return self._t != x
    def __reversed__(self):
        return reversed(self._t)
    def __rmul__(self,x):
        return x * self._t
    def copy(self):
        return self._t.copy()
    def count(self,*args,**kwargs):
        return self._t.count(*args,**kwargs)
    def index(self,*args,**kwargs):
        return self._t.index(*args,**kwargs)

class ReadOnlyDictProxy(ReadOnlyProxyType):
    def __init__(self,d):
        if not issubclass(type(d),dict):
            raise TypeError("'%s' only supports dicts, not '%s'." % (type(self).__name__,type(d).__name__))
        self._t = d
    def __contains__(self,*a,**kw):
        return self._t.__contains__(*a,**kw)
    def __eq__(self,*a,**kw):
        return self._t.__eq__(*a,**kw)
    def __format__(self,*a,**kw):
        return self._t.__format__(*a,**kw)
    def __getitem__(self,*a,**kw):
        return self._t.__getitem__(*a,**kw)
    def __iter__(self,*a,**kw):
        return self._t.__iter__(*a,**kw)
    def __len__(self,*a,**kw):
        return self._t.__len__(*a,**kw)
    def __ne__(self,*a,**kw):
        return self._t.__ne__(*a,**kw)
    def copy(self,*a,**kw):
        return self._t.copy(*a,**kw)
    def get(self,*a,**kw):
        return self._t.get(*a,**kw)
    def items(self,*a,**kw):
        return self._t.items(*a,**kw)
    def keys(self,*a,**kw):
        return self._t.keys(*a,**kw)
    def values(self,*a,**kw):
        return self._t.values(*a,**kw)
