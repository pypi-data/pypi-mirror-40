class AList(object):
    """An Association List class abstraction - implements most methods that work on a dict object"""
    def __init__(self, **kwargs):
        """Takes a list of keyword arguments for construction"""
        self._value = []
        keys=[]
        for key, value in kwargs.items():
            # Raising on multiple keys isn't standard
            # {"x": 1, "x": 2"} == {"x": 2}
            # But this is probably less surprising:
            if key in keys:
                raise ValueError('Key used multiple times.')
            self._value.append((key, value))
            keys.append(key)
        self._value = tuple(self._value)

    def __repr__(self):
        """Returns a human-readable representation"""
        # print(AList)
        return 'AList{}'.format(self._value.__repr__())

    def __contains__(self, key):
        """Check to see if a key is in the AList"""
        # For x in AList()
        for cell in self._value:
            if cell[0] == key:
                return True
        return False

    def __iter__(self):
        """Iterate over the AList"""
        return self

    def __next__(self):
        """Used as part of iteration to return the next AList item"""
        # For x in AList
        if not hasattr(self, '_iterindex'):
            self._iterindex = -1
        self._iterindex = self._iterindex + 1
        try:
            return self._value[self._iterindex]
        except IndexError:
            delattr(self, '_iterindex')
            raise StopIteration()

    def __len__(self):
        """Return the length of the AList as a positive or 0 integer"""
        # len(AList)
        return len(self._value)

    def __getitem__(self, key):
        """Return a value for a key"""
        # Alist['x']
        return self.index(key)

    def __setitem__(self, key, value):
        """Set a key-value pair"""
        # AList['x'] = v
        tmp = list(self._value)
        for cell in tmp:
            if cell[0] == key:
                new = [x for x in self._value if x[0] != key]
                new.append((key, value))
                self._value = tuple(new)
                return value
        tmp.append((key, value))
        self._value = tuple(tmp)
        return value

    def __delitem__(self, key):
        """Remove a key value pair by key"""
        #del Alist[key]
        for cell in self._value:
            if cell[0] == key:
                new = tuple([x for x in self._value if x[0] != key])
                self._value = new
                return None
        raise KeyError

    def index(self, key):
        """Get a value by key"""
        for cell in self._value:
            if cell[0] == key:
                return cell[1]
        raise KeyError

    def keys(self):
        """Return a tuple of keys in the AList"""
        k = []
        for cell in self._value:
            k.append(cell[0])
        return tuple(k)

    def values(self):
        """Return a tuple of values in the AList"""
        v = []
        for cell in self._value:
            v.append(cell[1])
        return tuple(v)

    def items(self):
        """Return a tuple of key-value tuples"""
        return self._value

    def get(self, key, default=None):
        """Return a key's value or a default value"""
        for cell in self._value:
            if cell[0] == key:
                return cell[1]
        return default

    def clear(self):
        """Remove all items from the AList"""
        self._value = tuple()

    def setdefault(self, key, default=None):
        """Set key to default if not in AList"""
        for cell in self._value:
            if cell[0] == key:
                return default
        new = list(self._value)
        new.append((key, default))
        self._value = tuple(new)
        return default

    def pop(self, key, default=KeyError):
        """Remove key and return value or default"""
        val = False
        new = False
        # Check for key
        for cell in self._value:
            if cell[0] == key:
                new = tuple([x for x in self._value if x[0] != key])
                val = cell[1]
                break
        # If we got something,
        # 'Mutate' ourselves
        # And return the value
        if val or new:
            self._value = new
            return val

        # Is default an exception? Raise it
        try:
            raise default
        # Not an exception. Return it.
        except TypeError:
            return default

    def popitem(self):
        """Remove and return 1st key-value tuple"""
        if len(self._value) > 0:
            val = self._value[0]
            new = tuple([x for x in self._value if x[0] != val[0]])
            self._value = new
            return val
        else:
            raise KeyError("popitem(): AList is empty")

    def copy(self):
        """Return a copy"""
        x = AList()
        x._value = self._value
        return x

    def update(self, alist2):
        """Add another AList to this AList"""
        if type(alist2) != AList:
            raise TypeError("update(): Expected an AList")
        for k, v in alist2:
            self.__setitem__(k, v)
