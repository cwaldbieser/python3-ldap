# Created on 2013.05.23
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

from ldap3 import AUTH_SIMPLE, STRATEGY_SYNC, STRATEGY_ASYNC_THREADED, STRATEGY_SYNC_RESTARTABLE, STRATEGY_REUSABLE_THREADED

test_server = 'sorintest.cloudapp.net'  # the ldap server where tests executed
test_user = 'john.doe@AD.SBARNEA.COM'  # the user that performs the tests
test_password = 'a3sv42vAS2vl'  # user's password

test_user = 'sorin.sbarnea@AD.SBARNEA.COM'  # the user that performs the tests
test_password = '1!sorinsorin2'  # user's password

test_base = 'o=test'  # base context where test objects are created
test_moved = 'ou=moved,o=test'  # base context where  objects are moved in ModifyDN operations
test_name_attr = 'cn'  # naming attribute for test objects

test_port = 10389  # ldap port
test_port_ssl = 8443 # 10636  # ldap secure port
test_authentication = AUTH_SIMPLE  # authentication type
test_check_names = False  # check attribute names in operations
test_get_info = False  # get info from DSA
test_lazy_connection = False  # connection lazy
test_strategy = STRATEGY_SYNC  # strategy for executing tests
#test_strategy = STRATEGY_ASYNC_THREADED  # uncomment this line to test the async strategy
#test_strategy = STRATEGY_SYNC_RESTARTABLE  # uncomment this line to test the sync_restartable strategy
#test_strategy = STRATEGY_REUSABLE_THREADED  # uncomment this line to test the sync_reusable_threaded strategy

# while testing against the serintest.cloudapp.net AD server, the strategy that worked better was the last one.

def dn_for_test(base, name):
    return test_name_attr + '=' + name + ',' + base
