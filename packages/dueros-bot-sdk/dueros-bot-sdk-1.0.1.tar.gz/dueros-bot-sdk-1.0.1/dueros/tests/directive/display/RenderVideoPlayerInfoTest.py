# encoding: utf8

import json
import unittest
from dueros.directive.Display.RenderVideoPlayerInfo import RenderVideoPlayerInfo

from dueros.directive.VideoPlayer.VideoPlayerInfoContent import VideoPlayerInfoContent
from dueros.directive.AudioPlayer.Control.PlayPauseButton import PlayPauseButton
from dueros.directive.AudioPlayer.Control.RepeatButton import RepeatButton
from dueros.directive.AudioPlayer.Control.ShowPlayListButton import ShowPlayListButton


class RenderVideoPlayerInfoTest(unittest.TestCase):

    def setUp(self):
        self.renderVideoPlayerInfo = RenderVideoPlayerInfo()

    def testGetData(self):

        with open('../../json/render_video.json', encoding='utf-8') as f:
            content = f.read()
            self.data = json.loads(content)
        print(self.data)

        content = VideoPlayerInfoContent('title')
        content.set_media_length_in_milliseconds(10000)
        playPauseButton = PlayPauseButton()
        playlistButton = ShowPlayListButton()
        controls = [playPauseButton, playlistButton]

        self.renderVideoPlayerInfo.set_token('test_token')
        self.renderVideoPlayerInfo.set_content(content)
        self.renderVideoPlayerInfo.set_controls(controls)
        self.assertEqual(self.renderVideoPlayerInfo.get_data(), self.data)
    pass
