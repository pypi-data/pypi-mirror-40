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
:mod:`Categories` -- Define categories for plugins

.. module:: Categories
   :platform: Unix, Windows
   :synopsis: Define categories for plugins
.. moduleauthor:: Micha Grandel <talk@michagrandel.de>
"""

from __future__ import unicode_literals, print_function
from io import open
import sys
from typing import *
from yapsy.IPlugin import IPlugin
import logging


class Server(IPlugin):
    """ applies fixes for a server """

    def __init__(self, logger: logging.Logger = None, **kwargs: Any) -> None:
        """
        :param logger: logger instance
        :param **kwargs: additional options
        """
        super().__init__()
        self.logger = logger
        if not self.logger:
            self.logger = logging.getLogger(__class__.__qualname__)
            self.logger.setLevel(logging.WARNING)
            self.logger.addHandler(logging.StreamHandler())
            self.logger.handlers[-1].setLevel(logging.WARNING)
        self.verbose = kwargs.get('verbose', 0)

    def fix(self, fix: AnyStr = None, force: bool = False) -> None:
        """
        apply fixes for a server

        :param fix: fix to apply; apply all if fix is None
        :param force: force to apply fix even if the script is running on a different server
        :param **kwargs: additional options
        """
        pass

    def identify(self) -> None:
        """
        Identify a server of a category

        :return: True, if it is a server of a specified category, else False
        """
        pass