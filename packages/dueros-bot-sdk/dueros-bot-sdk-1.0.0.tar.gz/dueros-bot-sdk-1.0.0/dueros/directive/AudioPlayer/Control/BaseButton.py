# encoding: utf8

class BaseButton:

    def __init__(self, button_type, name):
        self.data = {}
        self.data['type'] = button_type
        self.data['name'] = name

    def get_data(self):

        return self.data
