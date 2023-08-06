# encoding: utf8
import unittest
from dueros.directive.AudioPlayer.Control.RepeatButton import RepeatButton
from dueros.directive.AudioPlayer.Control.RepeatButtonEnum import RepeatButtonEnum


class RepeatButtonTest(unittest.TestCase):

    def setUp(self):
        self.repeatButton = RepeatButton()
        self.repeatButton.set_selected_value(RepeatButtonEnum.REPEAT_ONE)

    def testGetData(self):

        ret = {
            'type': 'RADIO_BUTTON',
            'name': 'REPEAT',
            'selectedValue': 'REPEAT_ONE'

        }

        self.assertEqual(self.repeatButton.get_data(), ret)
    pass
