# encoding: utf8

from dueros.directive.AudioPlayer.PlayerInfo import PlayerInfo


class AudioPlayerInfo(PlayerInfo):

    def __init__(self, content, controls=[]):
        super(AudioPlayerInfo, self).__init__(content, controls)
