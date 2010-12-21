import sys
import travel.trains

def main():
    if len(sys.argv) != 4:
        sys.stderr.write('Usage: %s <from_station> <to_station> <time>\n'
                % sys.argv[0])
        sys.exit(1)
    print travel.trains.get_train_info(*sys.argv[1:])
