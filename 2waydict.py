#!/usr/bin/env/python

# This module provides a bidirectional dictionary

__author__ = "Shrikrishna Holla <myself@shrikrishnaholla.in>"

import collections

class BiDiDict(dict):
    """
    Bidirectional dictionary
    ========================
    This class provides for a two way access of the dictionary
    For example, if the user-created dictionary is
    bidi = BiDiDict({
        "a"     : 1000,
        "b"     : 2000,
        "c"     : 1000,
        1000    : "d"
    })
    then the possible queries and their respective outputs are as follows -

    >>> bidi["a"]
    1000

    >>> bidi[1000]
    d

    >>> bidi["a":]
    1000

    >>> bidi[1000:]
    d

    >>> bidi[:1000]
    ('a', 'c')

    >>> bidi[:"d"]
    (1000,)

    >>> bidi[:2000]
    ('b',)

    It also gives you two new functions - replaceVal and replaceKey
    replaceVal => replaces every instance of old value with new value
    replaceKey => replaces old key with new key
    """

    # Thanks to Tim Wegener <twegener@radlogic.com.au> http://www.radlogic.com/releases/two_way_dict.py
    def __init__(self, *args, **kwargs):
        # Run dict's constructor
        dict.__init__(self)

        # It appears that dict.__init__ does not call self.update,
        # so need to do that here.
        self.update(*args, **kwargs)

    def __setitem__(self, key, value):
        if not isinstance(value, collections.Hashable):
            raise ValueError('Value must be hashable too, for bidirectional dictionary mapping')
        dict.__setitem__(self, key, value)

    # thanks to Terry Reedy and https://bitbucket.org/jab/bidict/src/tip/bidict.py

    def __getitem__(self, keyorslice):
        try:
            start, stop, step = keyorslice.start, keyorslice.stop, keyorslice.step
        except AttributeError:
            # keyorslice is a key, e.g. b[key]
            return dict.__getitem__(self, keyorslice)

        # keyorslice is a slice
        if (not ((start is None) ^ (stop is None))) or step is not None:
            raise TypeError('Slice must specify one of start or stop, not both')

        if start is not None: # forward lookup (by key), e.g. b[key:]
            return dict.__getitem__(self, start)

        # inverse lookup (by val), e.g. b[:val]
        assert stop is not None
        def _checkVal(kvtuple):
            if kvtuple[1] == stop:
                return kvtuple[0]

        return tuple([key for key, val in filter(_checkVal, dict.items(self))])

    def replaceKey(self, oldKey, newKey):
        if not oldKey in dict.keys(self):
            raise KeyError("oldKey doesn't exist")
        val = self.__getitem__(oldKey)
        self.__setitem__(newKey, val)
        dict.__delitem__(self, oldKey)

    def replaceVal(self, oldVal, newVal):
        for key in self[:oldVal]:
            self.__setitem__(key, newVal)

if __name__ == '__main__':
    """Unit Tests"""
    bidi = BiDiDict({
        "a"     : 1000,
        "b"     : 2000,
        "c"     : 1000,
        1000    : "d"    
    })

    print bidi["a"]
    print bidi[1000]
    print bidi["a":]
    print bidi[1000:]
    print bidi[:1000]
    print bidi[:"d"]
    print bidi[:2000]

    
    bidi.replaceKey(1000, 3000)
    print bidi

    bidi.replaceVal(1000, 5000)
    print bidi