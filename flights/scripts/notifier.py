#!/usr/bin/env python

import smtplib
import sys

import flights.plugins

def main():
    if len(sys.argv) != 3:
        sys.stderr.write('Usage: %s <airport> <flight_number>\n' % sys.argv[0])
        sys.exit(1)

    airport = getattr(flights.plugins, sys.argv[1], None)
    flight_number = sys.argv[2]
    if not airport:
        sys.stderr.write('Airport %s plugin is not found.\n' % sys.argv[1])
        sys.exit(1)
    status = airport.get_flight_info(flight_number)['status']
    if not status:
        return
