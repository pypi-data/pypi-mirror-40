# encoding: utf8

import unittest
from dueros.directive.AudioPlayer.Control.FavoriteButton import FavoriteButton


class FavoriteButtonTest(unittest.TestCase):
    '''
    '''

    def setUp(self):
        self.favoriteButton = FavoriteButton()
        self.favoriteButton.set_enabled(False)
        self.favoriteButton.set_selected(True)

    def testGetData(self):

        ret = {
            'type': 'BUTTON',
            'name': 'FAVORITE',
            'enabled': False,
            'selected': True
        }

        self.assertEqual(self.favoriteButton.get_data(), ret)
