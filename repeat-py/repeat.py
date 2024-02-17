"""Repeat a command"""

import argparse
import signal
import subprocess


def parse_args(args=None):
    parser = argparse.ArgumentParser(description='Repeat a command')
    parser.add_argument('command', metavar='CMD', help='The command to run')
    parser.add_argument('-b', '--no-break', dest='no_break', action='store_true', help='Passthrough Ctrl+Break')
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', help='Do not print to console')
    parser.add_argument('-0', '--till-success', dest='till', action='store_const', const='success',
                        help='Repeat the command until it succeeds')
    parser.add_argument('-1', '--till-failure', dest='till', action='store_const', const='failure',
                        help='Repeat the command until it fails')
    parser.add_argument('-n', '--attempts', dest='attempts', type=int, default=float('inf'),
                        help='Maximum number of times to repeat')
    parser.add_argument('-d', '--direct', dest='shell', action='store_false', help='Do not use shell')

    return parser.parse_args(args)


def NO_OP(*_, **__):
    pass


def frange(n):
    i = 0
    while i < n:
        yield i
        i += 1


def pad_to(num, max):
    return str(num).rjust(len(str(max)), '0')


BREAK_CODE = 0xc000013a


def main():
    args = parse_args()
    out = NO_OP if args.quiet else print
    proc = None

    def signal_handler(signum, frame):
        nonlocal proc
        if proc:
            print('\n^Break')
            proc.send_signal(signal.SIGTERM)

    if args.no_break:
        signal.signal(signal.SIGBREAK, signal_handler)

    for idx in frange(args.attempts):
        if idx:
            if args.till == 'success':
                out('Retrying...')
            elif args.till == 'failure':
                out('Repeating...')
            out()

        counter = '' if args.attempts == float('inf') else f' {pad_to(idx + 1, args.attempts)}/{args.attempts}'
        out(f'Running{counter}: {args.command}')

        proc = subprocess.Popen(args.command, shell=args.shell)
        try:
            proc.communicate()
            return_code = proc.returncode
        except KeyboardInterrupt:
            return_code = BREAK_CODE
        if args.till == 'success':
            if not return_code:
                return
            out(f'Command failed with error code {return_code}. ', end='')
        if args.till == 'failure':
            if return_code:
                return return_code
            out('Command succeeded. ', end='')
        else:
            assert args.till is None
            out(f'Command exited with error code {return_code}')
    out(f'Reached maximum number of attempts {args.attempts}')


if __name__ == '__main__':
    raise SystemExit(main())
