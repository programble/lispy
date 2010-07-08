# Copyright 2010 Curtis McEnroe <programble@gmail.com>
# Licensed under the GNU GPLv3

class Scope:
    def __init__(self, parent=None):
        self.bindings = {}
        self.parent = parent

    def __getitem__(self, key):
        # If bound in this scope, return that
        if self.bindings.has_key(key):
            return self.bindings[key]
        # Otherwise, look for it in the parent scope
        elif self.parent:
            return self.parent[key]
        # If we have no parent, key is not bound at all
        else:
            raise NameError("name '%s' is not bound" % key)

    def __setitem__(self, key, value):
        # Will shadow any bindings in the parent scope
        self.bindings[key] = value

    def __delitem__(self, key):
        del(self.bindings[key])

    def __repr__(self):
        # For debugging...
        if self.parent:
            return repr(self.parent) + '\n' + repr(self.bindings)
        else:
            return repr(self.bindings)

    def has_key(self, key):
        return self.bindings.has_key(key)
