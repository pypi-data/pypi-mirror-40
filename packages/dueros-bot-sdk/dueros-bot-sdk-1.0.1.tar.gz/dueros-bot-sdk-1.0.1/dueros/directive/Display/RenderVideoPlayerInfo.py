# encoding: utf8
from dueros.directive.Display.BaseRenderPlayerInfo import BaseRenderPlayerInfo


class RenderVideoPlayerInfo(BaseRenderPlayerInfo):

    def __init__(self, content=None, controls=[]):
        super(RenderVideoPlayerInfo, self).__init__('Display.RenderVideoPlayerInfo', content, controls)
