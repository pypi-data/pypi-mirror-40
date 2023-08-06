# encoding: utf8

import unittest
from dueros.directive.AudioPlayer.Control.LyricButton import LyricButton


class LyricButtonTest(unittest.TestCase):

    def setUp(self):
        self.lyricButton = LyricButton()
        self.lyricButton.set_enabled(False)
        self.lyricButton.set_selected(True)

    def testGetData(self):

        ret = {
            'type': 'BUTTON',
            'name': 'LYRIC',
            'enabled': False,
            'selected': True
        }

        self.assertEqual(self.lyricButton.get_data(), ret)
    pass
