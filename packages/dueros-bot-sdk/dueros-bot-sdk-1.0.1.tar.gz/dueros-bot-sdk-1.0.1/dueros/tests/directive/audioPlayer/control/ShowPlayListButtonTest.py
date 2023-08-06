# encoding: utf8
import unittest
from dueros.directive.AudioPlayer.Control.ShowPlayListButton import ShowPlayListButton


class ShowFavoriteListButtonTest(unittest.TestCase):

    def setUp(self):
        self.showPlayListButton = ShowPlayListButton()
        self.showPlayListButton.set_enabled(False)
        self.showPlayListButton.set_selected(True)

    def testGetData(self):

        ret = {
            'type': 'BUTTON',
            'name': 'SHOW_PLAYLIST',
            'enabled': False,
            'selected': True

        }

        self.assertEqual(self.showPlayListButton.get_data(), ret)
    pass
