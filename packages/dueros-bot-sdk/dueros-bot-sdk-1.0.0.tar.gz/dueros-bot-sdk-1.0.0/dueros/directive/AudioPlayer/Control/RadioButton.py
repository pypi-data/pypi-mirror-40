# encoding: utf8

from dueros.directive.AudioPlayer.Control.BaseButton import BaseButton


class RadioButton(BaseButton):

    def __init__(self, name, selected_value=''):
        super(RadioButton, self).__init__('RADIO_BUTTON', name)
        self.set_selected_value(selected_value)

    def set_selected_value(self, selected_value):

        self.data['selectedValue'] = selected_value
