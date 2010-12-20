Flight Notifier
===============

Install
-------

system install as root:

::

    sudo python setup.py install

user install in ~/.local/bin/:

::

    python setup.py install --user

Setup: flight-notifier.cfg
--------------------------

::

    [flight-notifier]
    tempdir = /var/tmp/flight-notifier

    [smtp]
    server = smtp.gmail.com
    port = 587
    login = cee.wing@gmail.com
    password = password
    name = Flight Notifier
    email = cee.wing@gmail.com

Settings:

 * tempdir is a directory that flight-notifier can use to store data.

Airport plugins
---------------

Currently we only have:

 * Manchester
 * Amsterdam (Schiphol)

Command line usage
------------------

::

    flight-notifier manchester AB1234 -e recipient1@gmail.com,recipient2@gmail.com -c ~/flights-notifier.cfg

Crontab
-------

You can edit crontab by "crontab -e":

Check flight AB1234 in Manchester every 5 minutes on 20-21 December:

::

    */5 * 20-21 12 * flights-notifier manchester AB1234 -e recipient1@gmail.com,recipient2@gmail.com -c ~/flights-notifier.cfg
