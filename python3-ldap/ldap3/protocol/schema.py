"""
Created on 2013.09.11

@author: Giovanni Cannata

Copyright 2013 Giovanni Cannata

This file is part of Python3-ldap.

Python3-ldap is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Python3-ldap is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with Python3-ldap in the COPYING and COPYING.LESSER files.
If not, see <http://www.gnu.org/licenses/>.
"""

from os import linesep
import re
from ldap3 import CLASS_ABSTRACT, CLASS_STRUCTURAL, CLASS_AUXILIARY, ATTRIBUTE_USER_APPLICATION, ATTRIBUTE_DIRECTORY_OPERATION, ATTRIBUTE_DISTRIBUTED_OPERATION, ATTRIBUTE_DSA_OPERATION
from ldap3.protocol.oid import Oids

def constantToClassKind(value):
    if value == CLASS_STRUCTURAL:
        return 'STRUCTURAL CLASS'
    elif value == CLASS_ABSTRACT:
        return 'ABSTRACT CLASS'
    elif value == CLASS_AUXILIARY:
        return 'AUXILIARY CLASS'
    else:
        return 'unknown'


def constantToAttributeUsage(value):
    if value == ATTRIBUTE_USER_APPLICATION:
        return 'User Application'
    elif value == ATTRIBUTE_DIRECTORY_OPERATION:
        return "Directory operation"
    elif value == ATTRIBUTE_DISTRIBUTED_OPERATION:
        return 'Distributed operation'
    elif value == ATTRIBUTE_DSA_OPERATION:
        return 'DSA operation'
    else:
        return 'unknown'

def attributeUsageToConstant(value):
    if value == 'userApplications':
        return ATTRIBUTE_USER_APPLICATION
    elif value == 'directoryOperation':
        return ATTRIBUTE_DIRECTORY_OPERATION
    elif value == 'distributedOperation':
        return ATTRIBUTE_DISTRIBUTED_OPERATION
    elif value == 'dsaOperation':
        return ATTRIBUTE_DSA_OPERATION
    else:
        return 'unknown'

def quotedStringToList(quotedString):
        string = quotedString.strip()
        if string[0] == '(' and string[-1] == ')':
            string = string[1:-1]
        elements = string.split("'")
        return [element.strip("'").strip() for element in elements if element]

def oidsStringToList(oidString):
        string = oidString.strip()
        if string[0] == '(' and string[-1] == ')':
            string = string[1:-1]
        elements = string.split('$')
        return [element.strip() for element in elements if element]

def extensionToTuple(extensionString):
        string = extensionString.strip()
        name, _, values = string.partition(' ')
        return name, quotedStringToList(values)

def listToString(listObject):
    if isinstance(listObject, str):
        return listObject

    r = ''
    for element in listObject:
        r += (listToString(element) if isinstance(element, list) else str(element)) + ', '

    return r[:-2] if r else ''


class ObjectClassInfo():
    def __init__(self, oid = None, name = None, description = None, obsolete = False, superior = None, kind = None, mustContain = None, mayContain = None, extensions = None, experimental = None,
                 definition = None):
        self.oid = oid
        self.name = name
        self.description = description
        self.obsolete = obsolete
        self.superior = superior
        self.kind = kind
        self.mustContain = mustContain
        self.mayContain = mayContain
        self.extensions = extensions
        self.experimental = experimental
        self.rawDefinition = definition
        self._oidInfo = None

    @property
    def oidInfo(self):
        if self._oidInfo is None and self.oid:
            self._oidInfo = Oids.get(self.oid, '')

        return self._oidInfo if self._oidInfo else None


    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        r = 'ObjectClass ' + self.oid
        r += (' [' + constantToClassKind(self.kind) + '] ') if isinstance(self.kind, int) else ''
        r += (' [OBSOLETE]' + linesep) if self.obsolete else linesep
        r += ('  Short name: ' + listToString(self.name) + linesep) if self.name else ''
        r += ('  Description: ' + self.description + linesep) if self.description else ''
        r += ('  Must contain attributes: ' + listToString(self.mustContain) + linesep) if self.mustContain else ''
        r += ('  May contain attributes: ' + listToString(self.mayContain) + linesep) if self.mayContain else ''
        r += ('  Extensions:' + linesep + linesep.join(['    ' + s[0] + ': ' + listToString(s[1]) for s in self.extensions]) + linesep) if self.extensions else ''
        r += ('  Experimental:' + linesep + linesep.join(['    ' + s[0] + ': ' + listToString(s[1]) for s in self.experimental]) + linesep) if self.experimental else ''
        r += ('  OidInfo:' + str(self.oidInfo)) if self.oidInfo else ''
        return r

    @staticmethod
    def fromDefinition(objectClassDefinition):
        if not objectClassDefinition:
            return None

        if [objectClassDefinition[0] == ')' and objectClassDefinition[:-1] == ')']:
            splitted = re.split('( NAME | DESC | OBSOLETE| SUP | ABSTRACT| STRUCTURAL| AUXILIARY| MUST | MAY | X-| E-)', objectClassDefinition[1:-1])
            values = splitted[::2]
            separators = splitted[1::2]
            separators.insert(0, 'OID')
            defs = list(zip(separators, values))
            objectClassDef = ObjectClassInfo()
            for d in defs:
                key = d[0].strip()
                value = d[1].strip()
                if key == 'OID':
                    objectClassDef.oid = value
                elif key == 'NAME':
                    objectClassDef.name = quotedStringToList(value)
                elif key == 'DESC':
                    objectClassDef.description = value
                elif key == 'OBSOLETE':
                    objectClassDef.obsolete = True
                elif key == 'SUP':
                    objectClassDef.description = oidsStringToList(value)
                elif key == 'ABSTRACT':
                    objectClassDef.kind = CLASS_ABSTRACT
                elif key == 'STRUCTURAL':
                    objectClassDef.kind = CLASS_STRUCTURAL
                elif key == 'AUXILIARY':
                    objectClassDef.kind = CLASS_AUXILIARY
                elif key == 'MUST':
                    objectClassDef.mustContain = oidsStringToList(value)
                elif key == 'MAY':
                    objectClassDef.mayContain = oidsStringToList(value)
                elif key == 'X-':
                    if not objectClassDef.extensions:
                        objectClassDef.extensions = list()
                    objectClassDef.extensions.append(extensionToTuple('X-' + value))
                elif key == 'E-':
                    if not objectClassDef.experimental:
                        objectClassDef.experimental = list()
                    objectClassDef.experimental.append(extensionToTuple('E-' + value))
                else:
                    raise Exception('malformed Object Class Definition key:' + key)
            objectClassDef.rawDefinition = objectClassDefinition
            return objectClassDef
        else:
            raise Exception('malformed Object Class Definition')



class AttributeTypeInfo():
    def __init__(self, oid = None, name = None, description = None, obsolete = False, superior = None, equality = None, ordering = None, substring = None, syntax = None, singleValue = False, collective = False, noUserModification = False, usage = None, extensions = None, experimental = None,
                 definition = None):
        self.oid = oid
        self.name = name
        self.description = description
        self.obsolete = obsolete
        self.superior = superior
        self.equality = equality
        self.ordering = ordering
        self.substring = substring
        self.syntax = syntax
        self.singleValue = singleValue
        self.collective = collective
        self.noUserModification = noUserModification
        self.usage = usage
        self.extensions = extensions
        self.experimental = experimental
        self.rawDefinition = definition
        self._oidInfo = None

    @property
    def oidInfo(self):
        if self._oidInfo is None and self.oid:
            self._oidInfo = Oids.get(self.oid, '')

        return self._oidInfo if self._oidInfo else None


    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        r = 'AtrributeType ' + self.oid
        r += (' [OBSOLETE]' + linesep) if self.obsolete else ''
        r += ' [SINGLE VALUE]' if self.singleValue else ''
        r += ' [COLLECTIVE]' if self.collective else ''
        r += ' [NO USER MODIFICATION]' if self.noUserModification else ''
        r += linesep
        r += ('  Usage: ' + constantToAttributeUsage(self.usage) + linesep) if self.usage else ''
        r += ('  Short name: ' + listToString(self.name) + linesep) if self.name else ''
        r += ('  Description: ' + self.description + linesep) if self.description else ''
        r += ('  Equality rule: ' + listToString(self.equality) + linesep) if self.equality else ''
        r += ('  Ordering rule: ' + listToString(self.ordering) + linesep) if self.ordering else ''
        r += ('  Substring rule: ' + listToString(self.substring) + linesep) if self.substring else ''
        r += ('  Syntax ' + listToString(self.syntax) + linesep) if self.syntax else ''
        r += ('  Extensions:' + linesep + linesep.join(['    ' + s[0] + ': ' + listToString(s[1]) for s in self.extensions]) + linesep) if self.extensions else ''
        r += ('  Experimental:' + linesep + linesep.join(['    ' + s[0] + ': ' + listToString(s[1]) for s in self.experimental]) + linesep) if self.experimental else ''
        r += ('  OidInfo:' + str(self.oidInfo)) if self.oidInfo else ''
        return r

    @staticmethod
    def fromDefinition(attributeTypeDefinition):
        if not attributeTypeDefinition:
            return None

        if [attributeTypeDefinition[0] == ')' and attributeTypeDefinition[:-1] == ')']:
            splitted = re.split('( NAME | DESC | OBSOLETE| SUP | EQUALITY | ORDERING | SUBSTR | SYNTAX | SINGLE-VALUE| COLLECTIVE| NO-USER-MODIFICATION| USAGE | X-| E-)', attributeTypeDefinition[1:-1])
            values = splitted[::2]
            separators = splitted[1::2]
            separators.insert(0, 'OID')
            defs = list(zip(separators, values))
            attributeTypeDef = AttributeTypeInfo()
            for d in defs:
                key = d[0].strip()
                value = d[1].strip()
                if key == 'OID':
                    attributeTypeDef.oid = value
                elif key == 'NAME':
                    attributeTypeDef.name = quotedStringToList(value)
                elif key == 'DESC':
                    attributeTypeDef.description = value
                elif key == 'OBSOLETE':
                    attributeTypeDef.obsolete = True
                elif key == 'SUP':
                    attributeTypeDef.description = oidsStringToList(value)
                elif key == 'EQUALITY':
                    attributeTypeDef.equality = oidsStringToList(value)
                elif key == 'ORDERING':
                    attributeTypeDef.ordering = oidsStringToList(value)
                elif key == 'SUBSTR':
                    attributeTypeDef.substr = oidsStringToList(value)
                elif key == 'SYNTAX':
                    attributeTypeDef.syntax = oidsStringToList(value)
                elif key == 'SINGLE-VALUE':
                    attributeTypeDef.singleValue = True
                elif key == 'COLLECTIVE':
                    attributeTypeDef.collective = True
                elif key == 'NO-USER-MODIFICATION':
                    attributeTypeDef.noUserModification = True
                elif key == 'USAGE':
                    attributeTypeDef.usage = attributeUsageToConstant(value)
                elif key == 'X-':
                    if not attributeTypeDef.extensions:
                        attributeTypeDef.extensions = list()
                    attributeTypeDef.extensions.append(extensionToTuple('X-' + value))
                elif key == 'E-':
                    if not attributeTypeDef.experimental:
                        attributeTypeDef.experimental = list()
                    attributeTypeDef.experimental.append(extensionToTuple('E-' + value))
                else:
                    raise Exception('malformed Attribute Type Definition key:' + key)
            attributeTypeDef.rawDefinition = attributeTypeDefinition
            return attributeTypeDef
        else:
            raise Exception('malformed Attribute Type Definition')

    @staticmethod
    def _returnKind(classKind):
        if classKind == 0:
            return 'STRUCTURAL'
        elif classKind == 1:
            return 'ABSTRACT'
        elif classKind == 2:
            return 'AUXILIARY'
        else:
            return 'unknown'


class SchemaInfo():
    """
       This class contains info about the ldap server schema read from an entry (default entry is DSE)
       as defined in rfc 4512. Unkwnown attributes are stored in the "other" dict
    """

    def __init__(self, schemaEntry, attributes):
        self.schemaEntry = schemaEntry
        self.createTimeStamp = attributes.pop('createTimestamp', None)
        self.modifyTimeStamp = attributes.pop('modifyTimestamp', None)
        self.attributeTypes = [AttributeTypeInfo.fromDefinition(attributeTypeDef) for attributeTypeDef in attributes.pop('attributeTypes', [])]
        self.ldapSyntaxes = attributes.pop('ldapSyntaxes', None)
        self.objectClasses = [ObjectClassInfo.fromDefinition(objectClassDef) for objectClassDef in attributes.pop('objectClasses', [])]
        self.other = attributes

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        r = 'DSA Schema from: ' + self.schemaEntry + linesep
        r += ('  Attribute Types:' + linesep + '    ' + ', '.join([str(s) for s in self.attributeTypes]) + linesep) if self.attributeTypes else ''
        r += ('  Object Classes:' + linesep + '    ' + ', '.join([str(s) for s in self.objectClasses]) + linesep) if self.objectClasses else ''
        r += ('  LDAP Syntaxes:' + linesep + '    ' + ', '.join([str(s) for s in self.ldapSyntaxes]) + linesep) if self.ldapSyntaxes else ''
        r += 'Other:' + linesep

        for k, v in self.other.items():
            r += '  ' + k + ': ' + linesep
            if isinstance(v, str):
                r += v + linesep
            else:
                r += linesep.join(['    ' + str(s) for s in v]) + linesep
        return r
