`Build Status <https://travis-ci.org/dignio/py-smsframework-pswin>`__
`Pythons <.travis.yml>`__

SMSframework PSWinCom Provider
==============================

`PSWin <https://wiki.pswin.com/>`__ Provider for
`smsframework <https://pypi.python.org/pypi/smsframework/>`__.

Installation
============

Install from pypi:

::

   $ pip install smsframework_pswin

To receive SMS messages, you need to ensure that `Flask
microframework <http://flask.pocoo.org>`__ is also installed:

::

   $ pip install smsframework_pswin[receiver]

Initialization
==============

.. code:: python

   from smsframework import Gateway
   from smsframework_pswin import PswinProvider

   gateway = Gateway()
   gateway.add_provider('pswin', PswinProvider,
       user='dignio',
       password='123',
       hostname='foo.pswin.com',  # Defaults to 'simple.pswin.com'
       https=True
   )

Config
------

Source: /smsframework_pswin/provider.py

-  ``user: str``: Account username
-  ``password: str``: Account password
-  ``hostname: str``: Provider hostname
-  ``https: bool``: Use HTTPS for outgoing messages? Default: ``False``

Receivers
=========

Source: /smsframework_pswin/receiver.py

Message Receiver: /im
---------------------

Login to https://accountweb.pswin.com/ using your account details and
edit the section “Mobile Originated (MO) messages forwarding
configuration”

Protocol: HTTP Value: ``<protocol>://<server-name>/<provider-name>/im``

Status Receiver: /status
------------------------

Login to https://accountweb.pswin.com/ using your account details and
edit the section “Delivery Reports (DR) forwarding configuration”

Protocol: HTTP Value:
``<protocol>://<server-name>/<provider-name>/status``
