import re
import urllib2

def get_flight_info(flight_number):
    urls = ['http://www.schiphol.com/vluchtinfo/vertrek_en.htm',
            'http://www.schiphol.com/vluchtinfo/vertrek_na_en.htm',
            'http://www.schiphol.com/vluchtinfo/vertrek_en_morgen.htm',
            'http://www.schiphol.com/vluchtinfo/vertrek_na_en_morgen.htm'
            ]

    for url in urls:
        content = urllib2.urlopen(url).read()
        index = 0
        while 'FlightinfoDark' in content[index:]:
            # 25 is length of <TR class=FlightinfoDark>
            from_index = content.index('<TR class=FlightinfoDark>', index) + 25
            to_index = content.index('</TR>', from_index)
            index = from_index
            info = re.findall('<[^>]*>([^<]*)<[^>]*', content[from_index:to_index])
            info = [i.strip() for i in info]
            number = info[0]
            if (flight_number.lower() == number.lower() or
                    flight_number.lower() == number.replace(' ', '').lower()):
                return dict(zip(
                    ['flight', 'destination', 'schema', 'status', 'actual',
                        'hall', 'belt/row', 'gate'],
                    info))
