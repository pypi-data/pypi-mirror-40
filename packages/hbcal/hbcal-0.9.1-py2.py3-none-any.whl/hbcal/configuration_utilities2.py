from future.builtins import super
from collections import MutableSet

class AmbiguousKeyError(KeyError):
    """An exception class raised by AbbrevList if the supplied key could be
    used to provide two or more possible values."""
    pass


class AbbrevSet(MutableSet):
    """This class provides a set with lookup by key. Only the
    start of the key needs to be provided - if it matches one of the keys
    the key is returned. If it matches more than one key, an exception
    (AmbiguousKeyError) is raised."""

    def __getitem__(self, item):
        found = None
        for set_item in self:
            if set_item.startswith(item):
                if found is None:
                    found = set_item
                else:
                    raise AmbiguousKeyError
        if found is None:
            raise KeyError
        return found

    def __contains__(self, item):
        try:
            self[item]
        except KeyError:
            return False
        else:
            return True


class AllowedOnlySet(MutableSet):

    def __init__(self, iterable=None, **kwargs):
        if 'allowed' in kwargs:
            self.allowed = kwargs['allowed']
        if iterable is not None:
            for iter in iterable:
                if iter not in self.allowed:
                    raise KeyError
        super().__init__(self, iterable, **kwargs)


    def add(self, value):
        if value not in self.allowed:
            raise KeyError


class MutexRestrictedSet(MutableSet):

    def __init__(self, iterable = None, **kwargs):
        if 'mutex_groups' in kwargs:
            self.mutex_groups = kwargs['mutex_groups']
        super().__init(self, **kwargs)
        if iterable is not None:
            for iter in iterable:
                super().add(iter)


