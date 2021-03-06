#############
Project goals
#############

1. python3-ldap strictly conforms to the current RFCs for LDAP version 3 (from 4510 to 4519)

    * **Latest RFCs for LDAP** v3 (dated 2006) obsolete the previous RFCs specified in RFC3377 (2251-2256, 2829, 2830, 3371) for LDAP v3 and amend and clarify the LDAP protocol.

    * All the asn1 definitions from the RFC4511 have been rewritten because those in the pyasn1_modules package are not current with the RFC.

2. Platform independent (tested on Linux and Windows) architecture

    * The library should **run on Windows and Linux** and (possibly) other Unixes with any difference.

3. Based on **pure Python code**

    * I usually work on Linux and Windows boxes and each time I must install the current python-ldap library for Python 2 from different sources. On Windows I need a binary installation for python-ldap. This is annoying and time and resources consuming.

    * python3-ldap should instead be easily installed from source or from pypi using pip or a similar package manager on different platforms.

    * Using python3-ldap library **don't need a C compiler neither the openldap client library**

    * Installation should be the same on any platform.

    * Socket and thread programming should be appropriate for the platform used, with no changes needed in the configuration and in the exposed API..

    * python3-ldap library should depend on the standard library and the pyasn1 package only.

4. Compatible with Python 3 and Python 2

    * Development is done in **Python 3 native code**

    , The library should be **compatible with Python 2** (2.6 and successive)

    - Testing is done on Python 3 (3.3, 3.4)  and Python 2 (2.6, 2.7)

    - Unicode strings are appropriately managed in Python 3. In Python 2 bytes (str object) are returned.

5. Multiple *connection strategies* to choose from, either synchronous or asynchronous

    - The library has different ways to connect to the LDAP server (no-thread, single-threaded, multithreaded, ...). This is achieved with **pluggable** communication strategies that can be changed on a per-connection basis.

    - STRATEGY_SYNC, STRATEGY_ASYNC_THREADED, STRATEGY_LDIF_PRODUCER and STRATEGY_SYNC_RESTARTABLE are currently defined.

6. Simplified query construction language

    - I previously developed an **abstraction layer** for LDAP query. I'd like to have a generalized LDAP abstraction layer to simplify access to the LDAP data.

7. **Compatibility mode** for application using python-ldap

    - I have a number of projects using the python-ldap library. I'd like to move them to Python 3 without changing what I've already done for LDAP.

    - It should be (possibly) enough just to change the import from python-ldap to python3-ldap to use them on Python 3, at least for the LDAP components.
