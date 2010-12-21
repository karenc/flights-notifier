#!/usr/bin/env python

import ConfigParser
import optparse
import os
import smtplib
import sys

import travel.airports

def main():
    parser = optparse.OptionParser('Usage: %prog <airport> <flight_number>')
    parser.add_option('-e', '--email', dest='email',
            help='send notification to EMAIL', metavar='EMAIL')
    parser.add_option('-c', '--config', dest='configfile',
            help='use configuration file')
    options, args = parser.parse_args()
    if len(args) != 2:
        parser.print_help()
        sys.exit(1)

    airport = args[0]
    plugin = getattr(travel.airports, airport, None)
    flight_number = args[1]
    if not plugin:
        sys.stderr.write('Airport %s plugin is not found.\n' % airport)
        parser.print_help()
        sys.exit(1)
    status = plugin.get_flight_info(flight_number)
    if not status:
        return
    status = status['status']
    if 'Departed' in status:
        return

    config = None
    if options.configfile:
        config = ConfigParser.ConfigParser()
        config.read(options.configfile)

    tempdir = None
    old_status = None
    if config and config.has_section('flight-notifier'):
        tempdir = config.get('flight-notifier', 'tempdir')
        if not os.path.exists(tempdir):
            os.mkdir(tempdir)
        elif os.path.exists(os.path.join(tempdir, flight_number)):
            old_status = open(os.path.join(
                tempdir, flight_number)).read()

    if (options.email and
            config and config.has_section('smtp') and
            status != old_status):
        server = smtplib.SMTP(config.get('smtp', 'server'),
                config.getint('smtp', 'port'))
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(config.get('smtp', 'login'),
                config.get('smtp', 'password'))
        subject = 'Flight status: %s %s (%s)' % (
                airport, flight_number, status)
        for email in options.email.split(','):
            server.sendmail(config.get('smtp', 'email'),
                    email,
                    'From: %s <%s>\n'
                    'To: %s\n'
                    'Subject: %s\n\n%s\n\n'
                    '---\nSent from flights-notifier\n' % (
                        config.get('smtp', 'name'),
                        config.get('smtp', 'email'),
                        email, subject, subject))
        server.close()

        if tempdir:
            open(os.path.join(tempdir, flight_number), 'w').write(status)
