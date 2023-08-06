from argparse import ArgumentParser

import sys

from sockpuppet.ports import wait_for_server


def handle_wait(args):
    params = {}
    for name in 'address', 'port', 'timeout', 'poll_frequency':
        value = getattr(args, name)
        if value:
            params[name] = value
    try:
        wait_for_server(**params)
    except AssertionError as e:
        print(str(e))
        sys.exit(1)
    else:
        print('server on %s:%s is up' % (args.address, args.port))


def main():
    parser = ArgumentParser(description='sockpuppet command line tools')
    subparsers = parser.add_subparsers()

    description = 'Wait for a server to start up on a socket.'
    subparser = subparsers.add_parser('wait', help=description)
    subparser.description = description

    subparser.add_argument('-a', '--address', default='127.0.0.1')
    subparser.add_argument('-p', '--port', type=int, required=True)
    subparser.add_argument('--timeout', type=float)
    subparser.add_argument('--poll-frequency', type=float)
    subparser.set_defaults(func=handle_wait)

    args = parser.parse_args()
    args.func(args)

