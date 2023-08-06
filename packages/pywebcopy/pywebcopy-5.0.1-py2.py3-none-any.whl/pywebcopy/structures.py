# -*- coding: utf-8 -*-

"""
pywebcopy.structures
~~~~~~~~~~~~~~~~~~~~

Structures powering pywebcopy.

"""


__all__ = ['CaseInsensitiveDict', 'RobotsTxt']


from collections import MutableMapping

from six.moves.urllib.robotparser import RobotFileParser


class CaseInsensitiveDict(MutableMapping):
    """ Flexible dictionary which creates less errors
    during lookups.

    Examples:
        dict = CaseInsensitiveDict()
        dict['Config'] = 'Config'

        dict.get('config') => 'Config'
        dict.get('CONFIG') => 'Config'
        dict.get('conFig') => 'Config'
    """

    def __init__(self, data=None, **kwargs):
        self._store = dict()
        if data is None:
            data = {}
        self.update(data, **kwargs)

    def __setitem__(self, key, value):
        self._store[key.lower()] = value

    def __getitem__(self, key):
        return self._store[key.lower()]

    def __delitem__(self, key):
        del self._store[key.lower()]

    def __iter__(self):
        return (key for key, value in self._store.items())

    def __len__(self):
        return len(self._store)

    def __copy__(self):
        return CaseInsensitiveDict(self._store)

    def lower_case_items(self):
        return (
            (key.lower(), value) for key, value in self._store.items()
        )

    def __eq__(self, other):
        if isinstance(other, MutableMapping):
            other = CaseInsensitiveDict(other)
        else:
            raise NotImplementedError

        return dict(self.lower_case_items()) == dict(other.lower_case_items())


class RobotsTxt(RobotFileParser, object):
    """ Provides a error tolerant python form of robots.txt

    Example:
        >>> rp = RobotsTxt('*', url='http://some-site.com/robots.txt')
        >>> rp.can_fetch('/hidden/url_path')
        False
        >>> rp.can_fetch('/public/url_path/')
        True

    """

    def __init__(self, user_agent, url):
        self.url = url
        self.user_agent = user_agent
        super(RobotsTxt, self).__init__(self.url)

    def can_fetch(self, url, *args, **kwargs):
        if not self.url or url:
            return True
        else:
            super(RobotsTxt, self).can_fetch(self.user_agent, url)
