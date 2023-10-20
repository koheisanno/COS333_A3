import sys
import registrar
import argparse

def main():
    parser = argparse.ArgumentParser(
        description='The registrar application',
        allow_abbrev=False)
    parser.add_argument('port',
        help='the port at which the server should liste',
        type=int)

    try:
        print(parser.parse_args().port)
        port = parser.parse_args().port
        registrar.app.run(host='0.0.0.0', port=port, debug=True)
        
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()