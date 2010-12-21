import re
import urllib2

def get_train_info(from_station, to_station, time):
    url = ('http://yuzuki.vmsplice.net/~karen/train.cgi?departing=true'
            '&at=%s&to=%s' % (from_station, to_station))
    content = urllib2.urlopen(url).read()
    if '<table' not in content:
        return {}
    content = content[content.index('<table'):content.index('</table>')]
    train = []
    for t in re.split('<tr class=[^>]*>', content):
        if '<td>' not in t:
            continue
        matched = False
        for td in t.split('<td>')[1:]:
            info = re.sub('<[^>]*>', '', td).strip()
            if info == time or info.replace(':', '') == time:
                matched = True
            if matched:
                train.append(info)
    return dict(zip(
        ['due', 'destination', 'status', 'platform'], train))
