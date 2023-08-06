#!/usr/bin/env python3
""" test the server environment and apply fixes """

from __future__ import print_function, division, unicode_literals
import sys
import platform
import os
import locale
import logging
import gettext
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timezone
from argparse import ArgumentParser
import pkg_resources

from servertools import MittwaldServer, Uberspace
from servertools.appdirs import AppDirs, user_log_dir, user_config_dir


__status__ = 'development'
__author__ = 'Micha Grandel'
__version__ = '0.1'
__copyright__ = '<> with ❤ by Micha Grandel'
__license__ = 'Apache License, Version 2.0'
__contact__ = 'M.Grandel@musik-meyer.de'


def _log_default_handler(proc, log_dir='.'):
    
    log_dir = os.path.abspath(log_dir)
    try:
        os.makedirs(log_dir)
    except IOError as e:
        pass
    
    filename = os.path.join(log_dir, '{}.log'.format(os.path.splitext(proc)[0]))
    handlers = [
        TimedRotatingFileHandler(filename, when='midnight', backupCount=10, encoding='utf-8')
    ]
    
    if __status__ == 'development':
        fmt = '%(asctime)s [%(levelname)s] %(message)s (in %(filename)s)'
        handlers[0].setLevel(logging.DEBUG)
    else:
        fmt = '%(asctime)s [%(levelname)s] %(message)s'
        handlers[0].setLevel(logging.INFO)
    
    file_logformatter = logging.Formatter(fmt, datefmt='%x %X')
    handlers[0].setFormatter(file_logformatter)
    
    return handlers


def main(args=None):
    """ setup logging and start application """
    if args == None:
        args = sys.argv
        
    script_name = os.path.basename(sys.argv[0])
    logging_path = user_log_dir(os.path.splitext(script_name)[0], __author__, __version__)
    config_path = user_config_dir(os.path.splitext(script_name)[0], __author__, __version__)

    # set locale
    locale.setlocale(locale.LC_ALL, '')
    _locale = locale.getlocale(locale.LC_ALL)[0]
    locale_path = pkg_resources.resource_filename("servertools", "data/i18n".format(_locale))
    
    translate = gettext.translation('servertools', localedir=locale_path, languages=[locale.getlocale()[0], 'en'])
    translate.install()
    
    # setup logging
    handlers = _log_default_handler(proc=script_name, log_dir=logging_path)
    logging.basicConfig(level=logging.DEBUG, format='%(message)s', handlers=handlers)

    logger = logging.getLogger('{}_logger'.format(os.path.splitext(script_name)[0]))
    logger.setLevel(logging.DEBUG)
    
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARNING)
    stream_handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(stream_handler)

    # setup argument parser
    parser = ArgumentParser(prog=script_name)
    verbosity_parsergroup = parser.add_mutually_exclusive_group()
    verbosity_parsergroup.add_argument("-v", dest='verbosity', action="count", help=_("increase verbosity"), default=0)
    verbosity_parsergroup.add_argument("--silent", action="store_true", help=_("silent (no output to terminal)"))
    parser.add_argument("--version", action="version", help=_("print version and exit"))
    parser.add_argument("--log-file", metavar='FILEPATH', action="store", help=_("overwrite path to log file"))
    
    command_parsers = parser.add_subparsers()
    identify_parser = command_parsers.add_parser('identify', help=_('identify server'))
    
    # todo: set the choices to specifiy a server to identify to installed plugins (e.g. mittwald or uberspace)
    identify_parser.add_argument('--look-for', dest='look_for', metavar='SERVER', help=_('look for a specific server'),
                                 choices=['mittwald', 'uberspace'], default=False)
    
    # todo: add feature to fix server-specific problems
    # fix_parser = command_parsers.add_parser('fix', help=_('apply fixes for a server'))
    
    # parse arguments
    args = parser.parse_args(args[1:])
    
    # handle verbosity
    verbosity = max(0, min(3, args.verbosity))
    if args.silent:
        verbosity = -1

    logging_level = {
        -1: logging.CRITICAL,  # 50
        0: logging.WARNING,  # 30
        1: logging.INFO,  # 20
        2: logging.INFO,  # 20
        3: logging.DEBUG  # 10
    }.get(verbosity, logging.WARNING)
    stream_handler.setLevel(logging_level)
    
    # start application
    logger.debug(_("{} started at {:%X} on Python {} ({})").format(
        script_name, datetime.now(), platform.python_version(), platform.architecture()[0]
    ))
    logger.debug(_("Save logs to {}").format(logging_path))
    logger.debug(_("Load configurations from {}").format(config_path))

    mw = MittwaldServer(logger=logger, verbose = verbosity>1)
    uberspace = Uberspace(logger=logger, verbose = verbosity>1)

    # todo: make server identification extendable through plugins for identification
    if args.look_for == 'mittwald':
        logger.info(_('Mittwald - Webhosting. Einfach intelligent.') if mw.identify() else '')
    elif args.look_for == 'uberspace':
        logger.info(_('Uberspace - Running on asteroids!') if uberspace.identify() else '')
    else:
        # default behaviour
        if not(mw.identify() and uberspace.identify()):
            logger.info(_('unknown platform'))
    logger.debug("-"*80)


if __name__ == '__main__':
    main(sys.argv)
