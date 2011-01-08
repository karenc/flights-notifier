import ConfigParser
import cPickle
import optparse
import os
import sys

import travel.notifiers
import travel.trains

OLD_STATUS_FILE = 'trains.status'

def main():
    parser = optparse.OptionParser(
            'Usage: %s <from_station> <to_station> <time>')
    parser.add_option('-e', '--email', dest='email',
            help='send notification to EMAIL', metavar='EMAIL')
    parser.add_option('-c', '--config', dest='configfile',
            help='use configuration file')
    options, args = parser.parse_args()

    if len(args) != 3:
        parser.print_help()
        sys.exit(1)

    from_station, to_station, time = args
    status = travel.trains.get_train_info(from_station, to_station, time)
    if not status:
        return
    status = status['status']

    config = None
    if options.configfile:
        config = ConfigParser.ConfigParser()
        config.read(options.configfile)

    tempdir = None
    old_status = None
    if config and config.has_section('flights-notifier'):
        tempdir = config.get('flights-notifier', 'tempdir')
        if not os.path.exists(tempdir):
            os.mkdir(tempdir)
        elif os.path.exists(os.path.join(tempdir, OLD_STATUS_FILE)):
            f = open(os.path.join(tempdir, OLD_STATUS_FILE), 'rb')
            try:
                old_status = cPickle.load(f)
            except:
                old_status = {}
            f.close()
            old_status = old_status.get('%s->%s@%s' % (from_station,
                to_station, time))

    notified = False
    if (options.email and
            config and config.has_section('smtp') and
            status != old_status):
        subject = 'Train status: %s %s -> %s (%s)' % (
                time, from_station, to_station, status)
        message = '%s\n\n--\nSent from trains-notifier\n' % (
                subject)
        travel.notifiers.email.notify(
                config.get('smtp', 'server'),
                config.get('smtp', 'port'),
                config.get('smtp', 'login'),
                config.get('smtp', 'password'),
                config.get('smtp', 'name'),
                config.get('smtp', 'email'),
                options.email,
                subject, message)
        notified = True

    if notified and tempdir:
        if os.path.exists(os.path.join(tempdir, OLD_STATUS_FILE)):
            f = open(os.path.join(tempdir, OLD_STATUS_FILE), 'rb')
            try:
                out = cPickle.load(f)
            except:
                out = {}
            f.close()
        else:
            out = {}
        out['%s->%s@%s' % (from_station, to_station, time)] = status
        f = open(os.path.join(tempdir, OLD_STATUS_FILE), 'wb')
        cPickle.dump(out, f)
        f.close()
