import sys
import argparse
import registrar

def main():
    # add port argument
    parser = argparse.ArgumentParser(
        description='The registrar application',
        allow_abbrev=False)
    parser.add_argument('port',
        help='the port at which the server should liste',
        type=int)

    # parse port argument
    try:
        port = parser.parse_args().port
    except Exception:
        print('Port must be an integer.', file=sys.stderr)
        sys.exit(1)
    # run application
    try:
        registrar.app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
