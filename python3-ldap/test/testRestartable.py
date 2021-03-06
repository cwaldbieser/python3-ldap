# """
# Created on 2014.03.29
#
# @author: Giovanni Cannata
#
# Copyright 2014 Giovanni Cannata
#
# This file is part of python3-ldap.
#
# python3-ldap is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python3-ldap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with python3-ldap in the COPYING and COPYING.LESSER files.
# If not, see <http://www.gnu.org/licenses/>.

from time import sleep

import unittest

from ldap3.protocol.rfc4511 import LDAPDN, AddRequest, AttributeList, Attribute, AttributeDescription, AttributeValue, CompareRequest, AttributeValueAssertion, AssertionValue, ValsAtLeast1
from test import test_server, test_port, test_user, test_password, test_authentication, test_strategy, dn_for_test, test_base, test_lazy_connection

from ldap3 import Server, Connection, ServerPool, SEARCH_SCOPE_WHOLE_SUBTREE, STRATEGY_SYNC_RESTARTABLE, POOLING_STRATEGY_ROUND_ROBIN,  SEARCH_SCOPE_SINGLE_LEVEL, ALL_ATTRIBUTES
from ldap3.core.exceptions import LDAPException


class Test(unittest.TestCase):
    def test_restartable_invalid_server(self):
        hosts = [test_server, '127.0.0.1']
        search_results = []
        servers = [Server(host=host, port=636, use_ssl=True) for host in hosts]

        connection = Connection(ServerPool(servers, POOLING_STRATEGY_ROUND_ROBIN, active=True, exhaust=True), user=test_user, password=test_password, client_strategy=STRATEGY_SYNC_RESTARTABLE, lazy=test_lazy_connection, pool_name='pool1')

        with connection as c:
            c.search(search_base='o=test', search_filter='(cn=test*)', search_scope=SEARCH_SCOPE_WHOLE_SUBTREE, attributes='*')

            for resp in connection.response:
                if resp['type'] == 'searchResEntry':
                    search_results.append(resp['dn'])
        self.assertTrue(len(search_results) > 15)

    def test_restartable_invalid_server2(self):
        #hosts = ['sl08', 'sl09', 'sl10', 'idmprofiler', 'openldap', 'localhost', 'edir1', 'edir2', 'edir3']
        hosts = ['sl10', 'edir1', 'idmprofiler', test_server]  # faster
        search_results = []
        servers = [Server(host=host, port=389, use_ssl=False) for host in hosts]
        server_pool = ServerPool(servers, POOLING_STRATEGY_ROUND_ROBIN, active=True, exhaust=True)
        connection = Connection(server_pool, user=test_user, password=test_password, client_strategy=STRATEGY_SYNC_RESTARTABLE, lazy=False)
        connection.open()
        connection.bind()
        connection.search(search_base='o=test', search_filter='(objectClass=*)', search_scope=SEARCH_SCOPE_SINGLE_LEVEL)
        if connection.response:
            for resp in connection.response:
                if resp['type'] == 'searchResEntry':
                    search_results.append(resp['dn'])
        connection.unbind()
        self.assertTrue(len(search_results) > 15)

    # def test_restartable_pool(self):
    #     hosts = ['edir', 'edir2', 'edir3']
    #     search_results = []
    #     servers = [Server(host=host, port=389, use_ssl=False) for host in hosts]
    #     server_pool = ServerPool(servers, POOLING_STRATEGY_ROUND_ROBIN, active=True, exhaust=True)
    #     connection = Connection(server_pool, user=test_user, password=test_password, client_strategy=STRATEGY_SYNC_RESTARTABLE, lazy=False)
    #     connection.open()
    #     connection.bind()
    #     for x in range(10000):
    #         connection.search(search_base='o=test', search_filter='(objectClass=*)', attributes=ALL_ATTRIBUTES, search_scope=SEARCH_SCOPE_SINGLE_LEVEL)
    #         sleep(1)
