import urllib2
import json

def get_flight_info(flight_number):
    # Returns something like this:
    # {u'status': u'Final Boarding', u'aOrD': u'D', u'schdTime': u'16:40', u'schdDate': u'Monday, 20 December 2010', u'destination': u'Amsterdam', u'flightNumber': u'KL1088', u'terminal': u'T2'}
    url = 'http://www.manchesterairport.co.uk/flightinformation/departures.json'
    content = urllib2.urlopen(url).read()
    info = json.loads(content)
    for flight in info['flights']:
        if flight['flightNumber'].lower() == flight_number.lower():
            return flight
