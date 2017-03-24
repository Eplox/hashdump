import hashlib, os, sys, signal, argparse


parser = argparse.ArgumentParser()
parser.add_argument("path", help="full path", type=str)
parser.add_argument("-md5", help="md5 hash", action="store_true")
parser.add_argument("-sha1", help="sha1 hash", action="store_true")
parser.add_argument("-sha256", help="sha256 hash", action="store_true")
args = parser.parse_args()


def signal_handler(signal, frame):
    global stop
    print '\nAborting...'
    stop=1
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


def hashfile(fname, type):
    if type == 'sha256':
        hash = hashlib.sha256()
    if type == 'sha1':
        hash = hashlib.sha1()
    if type == 'md5':
        hash = hashlib.md5()
    try:
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash.update(chunk)
        return hash.hexdigest()
    except:
        return 'Unable to read:'


def checkfile(file):
    fmt = '{0:<70} {1:>8}'
    if args.sha256: 
        print fmt.format(hashfile(file, 'sha256'),os.path.abspath(file))
    if args.sha1: 
        print fmt.format(hashfile(file, 'sha1'),os.path.abspath(file))
    if args.md5: 
        print fmt.format(hashfile(file, 'md5'),os.path.abspath(file))


if __name__ == '__main__':
    stop=0
    try:
        dir = args.path.strip('\\').strip('"')
    except:
        sys.exit(1)
    if 'win' in sys.platform:
        o='\\'
    else:
        o='/'

    if os.path.isfile(dir):
        checkfile(dir)
    else:
        for root, dirs, files in os.walk(dir):
            for name in files:
                if stop == 1:
                    break
                else:
                    checkfile(root+o+name)
