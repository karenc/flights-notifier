#!/usr/bin/env python

import sys

from flights.plugins import manchester

def main():
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: %s <flight_number>\n' % sys.argv[0])
        sys.exit(1)

    print manchester.get_flight_info(sys.argv[1])
