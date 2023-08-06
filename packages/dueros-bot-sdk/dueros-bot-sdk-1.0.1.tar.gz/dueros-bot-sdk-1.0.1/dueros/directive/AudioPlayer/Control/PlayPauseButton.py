# encoding: utf8

from dueros.directive.AudioPlayer.Control.Button import Button


class PlayPauseButton(Button):

    def __init__(self):
        super(PlayPauseButton, self).__init__('PLAY_PAUSE')
