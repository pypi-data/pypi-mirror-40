# encoding: utf8

from dueros.directive.AudioPlayer.Control.Button import Button


class FavoriteButton(Button):

    def __init__(self):
        super(FavoriteButton, self).__init__('FAVORITE')
