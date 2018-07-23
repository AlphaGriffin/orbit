# Copyright (C) 2018 Alpha Griffin
# @%@~LICENSE~@%@

import ag.logging as log

def usage():
    print()
    print("Usage: orbit <command>")
    print()
    print("Where <command> is:")
    print("   help      - Display this usage screen")
    print()

from sys import argv, exit

if len(argv) < 2:
    usage()
    exit(1)
    
elif argv[1] == 'help':
    usage()

else:
    log.error("unknown command", command=argv[1])
    print("orbit: unknown command: " + argv[1])
    usage()
    exit(2)

