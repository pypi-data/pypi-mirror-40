from unittest import TestCase
import platform
import os
from typing import *

from Server import MittwaldServer

class TestMittwaldServer(TestCase):
    MITTWALD = False

    @classmethod
    def setUpClass(cls) -> None:
        """ prepare the unit test """
        cls.MITTWALD = 'gentoo-mw1' in platform.platform()
        existing_dirs = ['~/backup', '~/bin', '~/files', '~/home', '~/html', '~/logs']
        for path in existing_dirs:
            path = os.path.expanduser(path)
            if not os.path.isdir(path):
                cls.MITTWALD = False
                break

    def test__fix_server(self) -> None:
        self.fail("not implemented yet")

    def test_identify(self) -> None:
        identified = MittwaldServer.identify()
        self.assertTrue(identified) if TestMittwaldServer.MITTWALD else self.assertFalse(identified)
