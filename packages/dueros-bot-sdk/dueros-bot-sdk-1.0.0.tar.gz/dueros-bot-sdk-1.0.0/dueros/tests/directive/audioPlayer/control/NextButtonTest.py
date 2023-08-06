# encoding: utf8

import unittest
from dueros.directive.AudioPlayer.Control.NextButton import NextButton


class NextButtonTest(unittest.TestCase):

    def setUp(self):
        self.nextButton = NextButton()
        self.nextButton.set_enabled(False)
        self.nextButton.set_selected(True)

    def testGetData(self):

        ret = {
            'type': 'BUTTON',
            'name': 'NEXT',
            'enabled': False,
            'selected': True
        }

        self.assertEqual(self.nextButton.get_data(), ret)
    pass
