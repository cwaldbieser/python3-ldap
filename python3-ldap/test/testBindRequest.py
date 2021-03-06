# Created on 2013.05.16
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

from ldap3.protocol.rfc4511 import BindRequest, LDAPDN, AuthenticationChoice, Simple, Version
from ldap3 import Server, Connection, STRATEGY_REUSABLE_THREADED
from test import test_server, test_port, test_user, test_password, test_authentication, test_strategy


class Test(unittest.TestCase):
    def setUp(self):
        server = Server(test_server, test_port)
        self.connection = Connection(server, auto_bind=True, client_strategy=test_strategy, user=test_user, password=test_password, authentication=test_authentication, pool_name='pool1')

    def tearDown(self):
        self.connection.unbind()
        if self.connection.strategy_type == STRATEGY_REUSABLE_THREADED:
            self.connection.strategy.terminate()

    def test_bind(self):
        bind_req = BindRequest()
        bind_req['version'] = Version(3)
        bind_req['name'] = LDAPDN(test_user)
        bind_req['authentication'] = AuthenticationChoice().setComponentByName('simple', Simple(test_password))
        result = self.connection.post_send_single_response(self.connection.send('bindRequest', bind_req))
        if not isinstance(result, bool):
            self.connection.get_response(result)
        self.assertTrue(True)
