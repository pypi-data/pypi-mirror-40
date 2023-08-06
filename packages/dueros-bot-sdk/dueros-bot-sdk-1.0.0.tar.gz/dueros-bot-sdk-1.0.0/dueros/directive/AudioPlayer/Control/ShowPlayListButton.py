# encoding: utf8

from dueros.directive.AudioPlayer.Control.Button import Button


class ShowPlayListButton(Button):

    def __init__(self):
        super(ShowPlayListButton, self).__init__('SHOW_PLAYLIST')
