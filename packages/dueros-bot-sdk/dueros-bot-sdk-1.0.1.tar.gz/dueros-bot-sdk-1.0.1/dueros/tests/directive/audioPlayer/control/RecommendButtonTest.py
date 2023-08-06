# encoding: utf8

import unittest
from dueros.directive.AudioPlayer.Control.RecommendButton import RecommendButton


class RecommendButtonTest(unittest.TestCase):

    def setUp(self):
        self.recommendButton = RecommendButton()
        self.recommendButton.set_enabled(False)
        self.recommendButton.set_selected(True)

    def testGetData(self):

        ret = {
            'type': 'BUTTON',
            'name': 'RECOMMEND',
            'enabled': False,
            'selected': True

        }

        self.assertEqual(self.recommendButton.get_data(), ret)
    pass
