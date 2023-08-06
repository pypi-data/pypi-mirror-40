# encoding: utf8

from dueros.directive.Display.media.BaseMediaListItem import BaseMediaListItem


class AudioItem(BaseMediaListItem):

    def __init__(self, title, title_subtext1):
        super(AudioItem, self).__init__(title, title_subtext1)

    def set_music_video_tag(self, tag):
        """
        设置isMusicVideo
        :param tag:
        :return:
        """
        if isinstance(tag, bool):
            self.data['isMusicVideo'] = tag
