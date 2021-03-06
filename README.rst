Flights Notifier
================

Flights notifier can get the status of your flights and notify you the status.
When flights are likely to be delayed or cancelled, this script will allow you
to get the most up to date information easily so you can be more prepared for
your journey.

Install
-------

system install in debian / ubuntu:

::

    sudo dpkg -i deb_dist/python-flights-notifier_0.0.0-1_all.deb

system install as root:

::

    sudo python setup.py install

user install in ~/.local/bin/:

::

    python setup.py install --user

Setup: flights-notifier.cfg
--------------------------

::

    [flights-notifier]
    tempdir = /var/tmp/flights-notifier

    [smtp]
    server = smtp.gmail.com
    port = 587
    login = asdf@gmail.com
    password = password
    name = Travel Notifier
    email = asdf@gmail.com

Settings:

 * tempdir is a directory that flights-notifier can use to store data.

Airport plugins
---------------

Currently we only have:

 * Manchester
 * Amsterdam (Schiphol)

Writing a new airport plugin
----------------------------

To write a new airport plugin for the flights notifier, create a python file in
the airports/ directory with the airport name, e.g. travel/airports/hongkong.py.

The new plugin will need to be imported in travel/airports/__init__.py:

::

    import hongkong

in hongkong.py, you need define a function get_flight_info which takes a flight
number and returns some information in form of a dict.  Currently, only
"status" is looked at:

::

    def get_flight_info(flight_number):
        return {
            'status': 'Delayed',
            }

Command line usage
------------------

::

    flights-notifier manchester AB1234 -e recipient1@gmail.com,recipient2@gmail.com -c ~/flights-notifier.cfg

Crontab
-------

You can edit crontab by "crontab -e":

Check flight AB1234 in Manchester every 5 minutes on 20-21 December:

::

    */5 * 20-21 12 * flights-notifier manchester AB1234 -e recipient1@gmail.com,recipient2@gmail.com -c ~/flights-notifier.cfg

Trains Notifier
---------------

There is also a trains notifier script which notifies you status of your
trains (in the UK only).  Most useful to commuters.

To check the status of the train going from Leeds to York at 07:50 during
weekdays, in crontab:

::

    */5 7 * * mon-fri trains-notifier leeds york 07:50 -e recipient@gmail.com -c ~/flights-notifier.cfg
