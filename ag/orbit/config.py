# Copyright (C) 2018 Alpha Griffin
# @%@~LICENSE~@%@

"""Set up some variables for access to configuration.

A system-dependent user configuration directory is automatically created.
"""

#import ag.logging as log

from os import makedirs, path

from appdirs import AppDirs
dirs = AppDirs("orbit", "Alpha Griffin")

dir = dirs.user_config_dir
#log.debug("Starting up", configdir=dir)

if not path.exists(dir):
    #log.info("Running first-time setup for configuration...")

    #log.debug("Creating user config directory")
    makedirs(dir, exist_ok=True)

if not path.isdir(dir):
    #log.fatal("Expected a directory for configdir", configdir=dir)
    raise Exception("Not a directory: " + dir)

