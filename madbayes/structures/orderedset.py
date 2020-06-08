from collections.abc import Set, MutableSet


class OrderedSet(MutableSet):

    def __init__(self, iterable=None):
        self.values = []
        if iterable is not None:
            for item in iterable:
                self.add(item)

    def __len__(self):
        return len(self.values)

    def __contains__(self, key):
        return key in self.values

    def __getitem__(self, key):
        return self.values[key]

    def __delitem__(self, key) -> None:
        self.values.remove(key)

    def __iter__(self):
        return self.values.__iter__()

    def add(self, key):
        if key not in self.values:
            self.values.append(key)

    def discard(self, key):
        if key in self.values:
            self.values.remove(key)

    def pop(self, index=0):
        return self.values.pop(index)

    def intersection(self, other):
        if not isinstance(other, Set):
            other = set(other)
        return OrderedSet(self & other)

    def union(self, other):
        if not isinstance(other, Set):
            other = set(other)
        return OrderedSet(self | other)

    def difference(self, other):
        if not isinstance(other, Set):
            other = set(other)
        return OrderedSet(self - other)

    def __repr__(self):
        return str(self.values)

    def __eq__(self, other):
        return set(self) == set(other)
