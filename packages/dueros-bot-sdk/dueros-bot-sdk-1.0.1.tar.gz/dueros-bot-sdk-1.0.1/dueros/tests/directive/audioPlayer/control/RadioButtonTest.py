# encoding: utf8

import unittest
from dueros.directive.AudioPlayer.Control.RadioButton import RadioButton


class PlayPauseButtonTest(unittest.TestCase):

    def setUp(self):
        self.radioButton = RadioButton('radio')
        self.radioButton.set_selected_value('selected value')

    def testGetData(self):

        ret = {
            'type': 'RADIO_BUTTON',
            'name': 'radio',
            'selectedValue': 'selected value'
        }

        self.assertEqual(self.radioButton.get_data(), ret)
    pass
