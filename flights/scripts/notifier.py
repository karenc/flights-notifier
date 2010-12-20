#!/usr/bin/env python

import ConfigParser
import optparse
import smtplib
import sys

import flights.plugins

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

    airport = getattr(flights.plugins, args[0], None)
    flight_number = args[1]
    if not airport:
        sys.stderr.write('Airport %s plugin is not found.\n' % args[0])
        parser.print_help()
        sys.exit(1)
    status = airport.get_flight_info(flight_number)
    if not status:
        return
    status = status['status']
    if 'Departed' in status:
        return

    config = None
    if options.configfile:
        config = ConfigParser.ConfigParser()
        config.read(options.configfile)

    if options.email and config and config.has_section('smtp'):
        server = smtplib.SMTP(config.get('smtp', 'server'),
                config.getint('smtp', 'port'))
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(config.get('smtp', 'login'),
                config.get('smtp', 'password'))
        server.sendmail(config.get('smtp', 'email'),
                options.email,
                'From: %s <%s>\n'
                'To: %s\n'
                'Subject: Flight status: %s (%s)\n\n'
                '---\nSent from flights-notifier\n' % (
                    config.get('smtp', 'name'),
                    config.get('smtp', 'email'),
                    options.email, flight_number, status))
        server.close()
