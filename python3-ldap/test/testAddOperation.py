# Created on 2013.06.06
#
# @author: Giovanni Cannata
#
# Copyright 2013 Giovanni Cannata
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

import unittest
import pytest

from ldap3 import Server, Connection, STRATEGY_REUSABLE_THREADED
from test import test_server, test_port, test_user, test_password, test_authentication, test_strategy, test_base, dn_for_test, test_name_attr, test_lazy_connection, test_get_info, test_check_names


class Test(unittest.TestCase):
    def setUp(self):
        server = Server(host=test_server, port=test_port, allowed_referral_hosts=('*', True), get_info=test_get_info)
        self.connection = Connection(server, auto_bind=True, version=3, client_strategy=test_strategy, user=test_user, password=test_password, authentication=test_authentication, lazy=test_lazy_connection, pool_name='pool1', check_names=test_check_names)
        result = self.connection.delete(dn_for_test(test_base, 'test-add-operation'))
        if not isinstance(result, bool):
            self.connection.get_response(result)

    def tearDown(self):
        self.connection.unbind()
        if self.connection.strategy_type == STRATEGY_REUSABLE_THREADED:
            self.connection.strategy.terminate()
        self.assertFalse(self.connection.bound)

    @pytest.mark.skipif(True,  reason="needs rework")
    def test_add(self):
        result = self.connection.add(dn_for_test(test_base, 'test-add-operation'), 'iNetOrgPerson', {'objectClass': 'iNetOrgPerson', 'sn': 'test-add', test_name_attr: 'test-add-operation'})
        if not isinstance(result, bool):
            response, result = self.connection.get_response(result)
        else:
            response = self.connection.response
            result = self.connection.result

        self.assertTrue(result['description'] in ['success', 'entryAlreadyExists'])
