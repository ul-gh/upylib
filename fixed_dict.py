class FixedDict(object):
    def __init__(self, dictionary):
        self._dictionary = dictionary
    def __setitem__(self, key, item):
            if key not in self._dictionary:
                raise KeyError(f"The key {key} is not defined.")
            self._dictionary[key] = item
    def __getitem__(self, key):
        return self._dictionary[key]
    def __repr__(self):
        return self._dictionary.__repr__()
