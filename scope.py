# Copyright 2010 Curtis (Programble) <programble@gmail.com>
# Licensed under the GNU GPLv3

class Scope:
    def __init__(self, parent=None):
        # Dict of bindings
        self.bindings = {}
        # Parent scope (Global scope's Parent will be None)
        self.parent = parent

    def __getitem__(self, key):
        # If binding exists in this scope, return its value
        if self.bindings.has_key(key):
            return self.bindings[key]
        # If this is the global scope, the binding does not exist
        elif self.parent == None:
            raise NameError("name '%s' is not defined" % key)
        # Look for the binding in parent scope
        else:
            return self.parent[key]

    def __setitem__(self, key, value):
        # Will shadow any other bindings of the same name in parent scopes
        self.bindings[key] = value

    def __delitem__(self, key):
        del(self.bindings[key])

    def __repr__(self):
        # If this is the global scope, just return our bindings
        if self.parent == None:
            return repr(self.bindings)
        # Otherwise, return our parent's bindings and our bindings
        return repr(self.parent) + '\n' + repr(self.bindings)

