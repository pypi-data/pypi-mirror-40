#!/usr/bin/env python
# @formatter:off
#
#                                             ,,
#                                             db
#     \
#     _\,,          `7MM  `7MM  `7MMpMMMb.  `7MM  ,p6"bo   ,pW"Wq.`7Mb,od8 `7MMpMMMb.
#    "-=\~     _      MM    MM    MM    MM    MM 6M'  OO  6W'   `Wb MM' "'   MM    MM
#       \\~___( ~     MM    MM    MM    MM    MM 8M       8M     M8 MM       MM    MM
#      _|/---\\_      MM    MM    MM    MM    MM 8M       8M     M8 MM       MM    MM
#     \        \      MM    MM    MM    MM    MM YM.    , YA.   ,A9 MM       MM    MM
#                     `Mbod"YML..JMML  JMML..JMML.YMbmd'   `Ybmd9'.JMML.   .JMML  JMML.
#
#                     <> with ❤ by Micha Grandel (talk@michagrandel.de)
#
#                     Project:         https://github.com/michagrandel/servertools
#                     Report a bug:    https://github.com/michagrandel/servertools/issues
#                     Contribute:      https://github.com/michagrandel/servertools/wiki/Contribute
#
#                     -----------------------------------------------------------------
#
#                     Copyright 2019 Micha Grandel
#
#                     Licensed under the Apache License, Version 2.0 (the 'License');
#                     you may not use this file except in compliance with the License.
#                     You may obtain a copy of the License at
#
#                     http://www.apache.org/licenses/LICENSE-2.0
#
#                     Unless required by applicable law or agreed to in writing,
#                     software distributed under the License is distributed on an
#                     'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
#                     either express or implied. See the License for the specific
#                     language governing permissions and limitations under the License.
#
#                     -----------------------------------------------------------------
#                     @formatter:on

""" test the server environment and apply fixes """

from __future__ import print_function, division, unicode_literals
import sys
import platform
import os
import locale
import logging
import gettext
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from argparse import ArgumentParser
import pkg_resources

from typing import AnyStr, List
from yapsy.PluginManager import PluginManager
from yapsy.PluginInfo import PluginInfo

# sys.path.append(os.path.abspath('../servertools'))

from servertools.plugins import Server
from servertools.appdirs import AppDirs


__status__ = 'development'
__author__ = 'Micha Grandel'
__version__ = '1.0'
__copyright__ = '<> with ❤ by Micha Grandel'
__license__ = 'Apache License, Version 2.0'
__contact__ = 'michagrandel@googlemail.com'


def _log_default_handler(proc: AnyStr, log_dir: AnyStr = '.'):
    """
    provides a default handler for a Logger

    :param proc: name of the script
    :param log_dir: directory in which the log file will be saved; default: '.'
    """
    
    log_dir = os.path.abspath(log_dir)
    try:
        # create directory if it does not exist yet
        os.makedirs(log_dir)
    except IOError:
        pass
    
    # create Logger Objects
    filename = os.path.join(log_dir, '{}.log'.format(os.path.splitext(proc)[0]))  # type: AnyStr
    handlers = [
        TimedRotatingFileHandler(filename, when='midnight', backupCount=10, encoding='utf-8')
    ]  # type: List[TimedRotatingFileHandler]
    
    # add formatter and set level for the Logger Objects
    message_format = '%(asctime)s [%(levelname)s] %(message)s'  # type: AnyStr
    level = logging.DEBUG if __status__ == 'development' else logging.INFO  # type: int
    
    if __status__ == 'development':
        message_format += ' (in %(name)s.%(filename)s)'
    for i in range(len(handlers)):
        handlers[i].setLevel(level)
        handlers[i].setFormatter(logging.Formatter(message_format, datefmt='%x %X'))
    
    return handlers


def main(args: List[AnyStr] = None) -> int:
    """
    prepare and start application

    the main method is responsible for setting up the environment,
    i.e. to load translations, set a logger, parse the command line arguments,
    load configuration files and start the application.

    :param args: command line arguments; default: None
    :type args: List of strings
    """
    if not args:
        args = sys.argv
    
    script_name = os.path.basename(sys.argv[0])
    application = AppDirs(os.path.splitext(script_name)[0], appauthor=__author__, version=__version__, roaming=True)
    logging_path = application.user_data_dir
    config_path = application.user_config_dir
    
    # set locale
    locale.setlocale(locale.LC_ALL, '')
    _locale = locale.getlocale(locale.LC_ALL)[0]
    locale_path = pkg_resources.resource_filename("servertools", "data/i18n")
    
    translate = gettext.translation("servertools", localedir=locale_path, languages=[locale.getlocale()[0], 'en'])
    translate.install()
    _ = lambda s: s if '_' not in globals() else _
    
    # setup logging
    handlers = _log_default_handler(proc=script_name, log_dir=logging_path)
    logging.basicConfig(level=4, format="%(message)s", handlers=handlers)
    
    logger = logging.getLogger("{}_logger".format(os.path.splitext(script_name)[0]))
    logger.setLevel(logging.DEBUG)
    
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARNING)
    stream_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(stream_handler)
    
    # setup argument parser
    parser = ArgumentParser(prog=script_name)
    verbosity_parsergroup = parser.add_mutually_exclusive_group()
    verbosity_parsergroup.add_argument("-v", dest='verbosity', action="count", help=_("increase verbosity"), default=0)
    verbosity_parsergroup.add_argument("--silent", action="store_true", help=_("silent (no output to terminal)"))
    parser.add_argument("--version", action="version", help=_("print version and exit"))
    parser.add_argument("--log-file", metavar='FILEPATH', action="store", help=_("overwrite path to log file"))
    
    command_parsers = parser.add_subparsers(help="commands")
    identify_parser = command_parsers.add_parser("identify", add_help=False, parents=[parser])
    
    # load plugins for different server types
    plugins_directories = [
        pkg_resources.resource_filename("servertools", "plugins"),
        os.path.join(application.user_data_dir, 'plugins'),
        os.path.expanduser(os.path.normpath('~/.{appname}/plugins'.format(appname=application.appname)))
    ]
    sys.path.extend(plugins_directories)
    plugin_manager = PluginManager(directories_list=plugins_directories, plugin_info_ext='plugin')
    plugin_manager.setCategoriesFilter({"Server": Server, })
    plugin_manager.locatePlugins()
    plugin_manager.collectPlugins()
    
    # plugins to identify servers and fix problems that might happen on them
    plugins = plugin_manager.getPluginsOfCategory('Server')  # type: List[PluginInfo]
    
    # choices for the command line flag `--look-for`
    server_choices = []  # type: List[AnyStr]
    # set valid values for --look-for from installed plugins
    for plugin in plugins:
        commandline_argument = plugin.name.lower().replace('server', '').strip().replace(' ', '-')
        if len(commandline_argument) > 0:
            server_choices.append(commandline_argument)
        else:
            raise ValueError(_("Plugin {name} doesn't have a valid name!").format(name=plugin.name))
    
    identify_parser.add_argument("--look-for", metavar="SERVER", dest="look_for", help=_("look for a specific server"),
                                 choices=server_choices, default='')
    identify_parser.set_defaults(name="identify")
    
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
    verbose = logger.info if verbosity > 1 else logger.debug
    
    # start application
    logger.debug(_("{program} started at {started_at:%X} on Python {py_version} ({architecture})").format(
        program=script_name, started_at=datetime.now(), py_version=platform.python_version(),
        architecture=platform.architecture()[0]
    ))
    logger.debug(_("Verbosity Level at {verbosity}").format(verbosity=verbosity))
    
    plugins_information = {}
    for category in plugin_manager.getCategories():
        plugins_information[category] = list()
        for plugin in plugin_manager.getPluginsOfCategory(category):
            plugins_information[category].append({'name': plugin.name, 'author': plugin.author})
    
    # if verbosity > 1:
    logger.info(_("Save logs to {path}").format(path=logging_path))
    logger.info(_("Load configurations from {path}").format(path=config_path))
    logger.info(_('Look for plugins in:\n\t{path}').format(path=',\n\t'.join(plugins_directories)))
    verbose(_('Include {amount} Plugin Categories.').format(amount=len(plugin_manager.getCategories())))
    logger.debug(', '.join(plugin_manager.getCategories()))
    verbose(_('{amount} Plugin(s) loaded.').format(amount=len(plugins_information.keys())))
    
    for category in plugins_information:
        logger.debug('[{}]'.format(category))
        for cat in plugins_information[category]:
            logger.debug(_('\t{name} (by {author})').format(name=cat['name'], author=cat['author']))
        logger.debug('')
    
    for plugin in plugins:
        logger.debug(_("Try to identify {name}").format(name=plugin.name))
        command = plugin.name.lower().replace('server', '').strip().replace(' ', '-'),
        if args.look_for == command and plugin.plugin_object.identify():
            logger.debug(_("Successfully identified {name}").format(name=plugin.name))
            print("{} - {}".format(plugin.details.get('Server Info', 'Host'),
                                   plugin.details.get('Server Info', 'Slogan')))
            break
    else:
        print(_('Not {}').format(args.look_for) if len(args.look_for) > 0 else _('Unknown platform'))
        return 1
    logger.debug("-" * 80)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
