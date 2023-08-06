# encoding: utf8
from dueros.directive.Display.BaseRenderPlayerInfo import BaseRenderPlayerInfo


class RenderAudioPlayerInfo(BaseRenderPlayerInfo):

    def __init__(self, content=None, controls=[]):
        super(RenderAudioPlayerInfo, self).__init__('Display.RenderAudioPlayerInfo', content, controls)
