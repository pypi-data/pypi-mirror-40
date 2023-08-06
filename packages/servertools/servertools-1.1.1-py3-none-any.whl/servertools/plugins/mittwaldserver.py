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

"""
:mod:`MittwaldServer` -- classes and methods to identify and apply fixes to a Mittwalds Server

.. module:: MittwaldServer
   :platform: Unix, Windows
   :synopsis: classes and methods to identify and apply fixes to a Mittwalds Server
.. moduleauthor:: Micha Grandel <talk@michagrandel.de>
"""

from __future__ import unicode_literals, print_function
from io import open
import sys
from typing import *
import logging
import os
import platform

from servertools.plugins import Server


if '_' not in globals():
    _ = unicode if sys.version_info.major < 3 else str


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
        if not self.is_activated:
            return None
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
