# -*- coding: utf-8 -*-

"""
:mod:`Server` - provides classes and methods to identify a server environment and to fix its problems
"""

from __future__ import print_function, unicode_literals, division, absolute_import

import sys
import os
import platform
import logging
from typing import List, AnyStr, Any

_ = lambda s: s

class LoggableObject(object):
    """
    Loggable is an object with built-in support for logging
    """
    def __init__(self, logger: logging.Logger = None, **kwargs: Any) -> None:
        """
        :param logger: logger instance
        """
        super().__init__()
        self.logger = logger
        if not self.logger:
            self.logger = logging.getLogger(__class__.__qualname__)
            self.logger.setLevel(logging.WARNING)
            self.logger.addHandler(logging.StreamHandler())
            self.logger.handlers[-1].setLevel(logging.WARNING)
        self._verbose = kwargs.get('verbose', 0)


class Server(LoggableObject):
    """ applies fixes for a server """

    def __init__(self, logger: logging.Logger = None, **kwargs: Any) -> None:
        """
        :param logger: logger instance
        """
        super().__init__(logger, **kwargs)

    def apply(self, fix: AnyStr = None, force: bool = False) -> None:
        """
        apply fixes for a server

        :param fix: fix to apply; apply all if fix is None
        :param force: force to apply fix even if the script is running on a different server
        :param **kwargs: additional options
        """
        self._fix_server(fix=fix, force=force)

    def identify(self) -> None:
        """
        Identify a server of a category

        :return: True, if it is a server of a specified category, else False
        """
        pass


class MittwaldServer(Server):
    """ applies fixes for Mittwald server """

    def __init__(self, logger: logging.Logger = None, **kwargs: Any) -> None:
        """

        :param logger: logger object
        :type logger: :py:class:`~.logging.Logger`
        """
        super().__init__(logger, **kwargs)
        self._pythonpath = '~/files/.local/lib/site-packages'

    def apply(self, fix: AnyStr = None, force: bool = False) -> None:
        """
        apply fixes for a Mittwald server

        :param fix: fix to apply; apply all if fix is None
        :param force: force to apply fix even if the script is running on a different server
        :param **kwargs: additional options
        """
        # make sure, the ~/files/.local/lib/site-packages exists!
        if not self.identify():
            if not force:
                raise RuntimeWarning(_('To apply fixes for Mittwald to a foreign server, use the force-Parameter!'))
            else:
                self.logger.warning(_('Warning: Apply fixed for Mittwald to a foreign server!'))

        if os.path.isdir(os.path.expanduser(self._pythonpath)):
            os.makedirs(self._pythonpath)

        sys.path.append(os.path.expanduser(self._pythonpath))

    def identify(self) -> bool:
        """
        returns True, if running on a Mittwald Server

        :return: whether or not running on a Mittwald Server
        :rtype: bool
        """
        if self._verbose > 2:
            self.logger.info('Verifying Mittwald ...')
        
        mw = True if 'gentoo-mw' in platform.platform() else False
        if mw:
            msg = _("Can't find {}!")
            assert (os.path.isdir(os.path.expanduser('~/backup'))), msg.format("$HOME/backup")
            assert (os.path.isdir(os.path.expanduser('~/bin'))), msg.format("$HOME/bin")
            assert (os.path.isdir(os.path.expanduser('~/files'))), msg.format("$HOME/files")
            assert (os.path.isdir(os.path.expanduser('~/home'))), msg.format("$HOME/home")
            assert (os.path.isdir(os.path.expanduser('~/html'))), msg.format("$HOME/html")
            assert (os.path.isdir(os.path.expanduser('~/logs'))), msg.format("$HOME/logs")
            try:
                os.mkdir(os.path.expanduser('~/.test'))
                mkdir = True
            except PermissionError as e:
                mkdir = False
            assert (not mkdir), _("On Mittwald servers, you cannot create directories in the user's home directory!")
            if self._verbose > 1:
                self.logger.info("Mittwald - Webhosting. Einfach intelligent.")
        else:
            if self._verbose > 1:
                self.logger.info('Not Mittwald!')
        return mw


class Uberspace(Server):
    """ applies fixes for Uberspace """

    def __init__(self, logger: logging.Logger = None, **kwargs: Any) -> None:
        """

        :param logger: logger instance
        """
        super().__init__(logger, **kwargs)

    def apply(self, fix: AnyStr = None, force: bool = False) -> None:
        """
        apply fixes for an uberspace

        :param fix: fix to apply; apply all if fix is None
        :param force: force to apply fix even if the script is running on a different server
        :param **kwargs: additional options
        """
        pass

    def identify(self) -> bool:
        """
        returns True, if running on an uberspace

        :return: whether or not running on an uberspace
        :rtype: bool
        """
        if self._verbose > 2:
            self.logger.info('Verifying Uberspace ...')
        
        if 'uberspace' in platform.node():
            if self._verbose > 1:
                self.logger.info("Uberspace - Running on asteroids!")
            return True
        else:
            if self._verbose > 1:
                self.logger.info('Not uberspace!')
            return False
