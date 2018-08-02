# Copyright (C) 2018 Alpha Griffin
# @%@~LICENSE~@%@

'''Helpers for command-line interfaces'''

from contextlib import suppress
from sys import argv, exit


def main(run):
    with suppress(KeyboardInterrupt):
        try:
            run(argv[1:] if len(argv) > 1 else None)

        except (ValueError, TypeError) as e:
            print()
            print("{}: {}".format(argv[0], e))

def invoke(call, cmd, exit_val, run, args, args_min=0, args_max=0, pass_single=False, optional=False):
    if optional and args is None:
        pass

    elif args_min == 0 and args_max == 0:
        if args is not None:
            print()
            print("{} {}: Not expecting any arguments".format(call, cmd))
            exit(exit_val)

    elif args_min == args_max:
        if args is None or len(args) != args_min:
            print()
            print("{} {}: Expecting exactly {} argument{}".format(call, cmd, args_min,
                "" if args_min == 1 else "s"))
            exit(exit_val)

    else:
        if args is not None and (len(args) < args_min or len(args) > args_max):
            print()
            print("{} {}: Expecting no less than {} and no more than {} arguments".format(
                call, cmd, args_min, args_max))
            exit(exit_val)

    #try:
    run(args[0] if pass_single else args)

    #except (ValueError, TypeError) as e:
    #    print()
    #    print("{} {}: {}".format(call, cmd, e))
    #    exit(exit_val)

