
TRAP forwarder, SNMPv3 to SNMPv1
================================

In this configuration SNMP Proxy Forwarder receives SNMPv3 TRAP PDU
and forwards it as SNMPv1 TRAP PDU.

.. note::

    When forwarding SNMP notifications, server part receives TRAPs from SNMP
    agents, while client part forwards them towards Managers. This is opposite
    to SNMP commands forwarding where server parts is directed towards SNMP
    managers and client part talks to SNMP agents.

    This means that if you want to forward both SNMP command and notification
    packets, you'd need to run at least two pairs of servers and clients
    forwarding packets in opposite directions.

You could test this configuration by running:

.. code-block:: bash

    $ snmptrap -v3 -e 0x090807060504030201 -l authPriv -u test-user -a MD5 -A authkey1 -x DES -X privkey1 \
        127.0.0.1:1162 12345 1.3.6.1.2.5 sysDescr s myagent

.. toctree::
   :maxdepth: 2

Server configuration
--------------------

Server is configured to:

* listen on UDP socket at localhost
* expect SNMP TRAP packets sent over SNMPv3, USM user "test-user"
* forward all queries to snmpfwd client through an unencrypted trunk connection
  running in *client* mode

.. warning::

    Since SNMP TRAP is always a one-way communication, SNMPv3 parties can't
    negotiate authoritative SNMP engine ID automatically which is used
    for authentication and encryption purposes.

    When SNMPv3 authentication or encryption services are being used, it is
    required to statically configure
    :ref:`snmp-security-engine-id <snmp-security-engine-id-server-option>`
    (also known as *authoritative* SNMP engine ID) to match SNMP engine ID of
    the SNMP engine sending SNMP TRAP message.

.. literalinclude:: /../../conf/trap-forwarding-snmpv3-to-snmpv1/server.conf

:download:`Download </../../conf/trap-forwarding-snmpv3-to-snmpv1/server.conf>` server configuration file.

Client configuration
--------------------

Client is configured to:

* listen on server-mode unencrypted trunk connection
* place inbound TRAP PDUs into SNMP v1 messages and forward them to public
  SNMP manager running at *demo.snmplabs.com*

.. literalinclude:: /../../conf/trap-forwarding-snmpv3-to-snmpv1/client.conf

:download:`Download </../../conf/trap-forwarding-snmpv3-to-snmpv1/client.conf>` client configuration file.
