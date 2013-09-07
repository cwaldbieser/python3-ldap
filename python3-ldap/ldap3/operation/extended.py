"""
Created on 2013.05.31

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

from ldap3.protocol.rfc4511 import ExtendedRequest, RequestName, RequestValue, \
    ResultCode
from ldap3.protocol.convert import decodeReferrals


# ExtendedRequest ::= [APPLICATION 23] SEQUENCE {
#     requestName      [0] LDAPOID,
#     requestValue     [1] OCTET STRING OPTIONAL }


def extendedOperation(requestName, requestValue = None):
    request = ExtendedRequest()
    request['requestName'] = RequestName(requestName)
    if requestValue:
        request['requestValue'] = RequestValue(requestValue)

    return request


def extendedRequestToDict(request):
    return {
        'name': str(request['requestName']),
        'value': str(request['requestValue']) if request['requestValue'] else None
    }


def extendedResponseToDict(response):
    return {
        'result': int(response[0]),
        'dn': str(response['matchedDN']),
        'message': str(response['diagnosticMessage']),
        'description': ResultCode().getNamedValues().getName(response[0]),
        'referrals': decodeReferrals(response['referral']),
        'responseName': str(response['responseName']),
        'responseValue': str(response['responseValue'])
    }


def intermediateResponseToDict(response):
    return {
        'responseName': str(response['responseName']),
        'responseValue': str(response(['responseValue']))
    }