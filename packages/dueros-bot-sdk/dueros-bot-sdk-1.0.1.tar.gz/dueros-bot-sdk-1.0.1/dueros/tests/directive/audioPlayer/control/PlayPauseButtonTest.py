# encoding: utf8

import unittest
from dueros.directive.AudioPlayer.Control.PlayPauseButton import PlayPauseButton


class PlayPauseButtonTest(unittest.TestCase):

    def setUp(self):
        self.playPauseButton = PlayPauseButton()
        self.playPauseButton.set_enabled(False)
        self.playPauseButton.set_selected(True)

    def testGetData(self):

        ret = {
            'type': 'BUTTON',
            'name': 'PLAY_PAUSE',
            'enabled': False,
            'selected': True
        }

        self.assertEqual(self.playPauseButton.get_data(), ret)
    pass
