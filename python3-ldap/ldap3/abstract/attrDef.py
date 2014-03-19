"""
Created on 2014.01.11

@author: Giovanni Cannata

Copyright 2014 Giovanni Cannata

This file is part of python3-ldap.

python3-ldap is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

python3-ldap is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with python3-ldap in the COPYING and COPYING.LESSER files.
If not, see <http://www.gnu.org/licenses/>.
"""
from ldap3 import LDAPException


class AttrDef(object):
    """
    Attribute definition for abstract layer:
    'name' is the real attribut name
    'key' is the friendly name to use in query and while accessing the attribute, if not set is the same of name
    'default' is the value returned if the attribute is not present
    'validate' is an optional callable, called to check if the value in the query is valid, the callable is called with the value parameter
    'preQuery' is an optional callable, called to transform values to be searched
    'postQuery' is an optional callable, called to transform values returned by search
    'dereference_dn' is a reference to an ObjectDef instance. When the attribute value contains a dn it will be searched and substituted in the entry
    AttrDef('name') creates an AttrDef object for attribute 'name' with all default values
    """

    def __init__(self, name, key=None, validate=None, pre_query=None, post_query=None, default=None, dereference_dn=None):
        self.name = name
        self.key = ''.join(key.split()) if key else name  # key set to name if not present
        self.validate = validate
        self.pre_query = pre_query
        self.post_query = post_query
        self.default = default
        self.dereference_dn = dereference_dn

    def __repr__(self):
        r = 'AttrDef(key={0.key!r}'.format(self)
        r += ', name={0.name!r}'.format(self)
        r += '' if self.validate is None else ', validate={0.validate!r}'.format(self)
        r += '' if self.pre_query is None else ', pre_query={0.pre_query!r}'.format(self)
        r += '' if self.post_query is None else ', post_query={0.post_query!r}'.format(self)
        r += '' if self.default is None else ', default={0.default!r}'.format(self)
        r += '' if self.dereference_dn is None else ', dereference_dn={0.dereference_dn!r}'.format(self)
        r += ')'

        return r

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if isinstance(other, AttrDef):
            return self.key == other.key

        return False

    def __lt__(self, other):
        if isinstance(other, AttrDef):
            return self.key < other.key

        return False

    def __hash__(self):
        if self.key:
            return hash(self.key)
        else:
            return id(self)  # unique for each istance

    def __setattr__(self, key, value):
        if hasattr(self, 'key') and key == 'key':  # key cannot be changed because is being used for __hash__
            raise LDAPException('key already set')
        else:
            object.__setattr__(self, key, value)