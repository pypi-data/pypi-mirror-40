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
from servertools.plugins import Server
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
