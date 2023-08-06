# encoding: utf8

from dueros.directive.Display.tag.BaseTag import BaseTag
from dueros.directive.Display.tag.TagTypeEnum import TagTypeEnum


class FreeTag(BaseTag):

    def __init__(self):
        super(FreeTag, self).__init__(TagTypeEnum.TAG_TYPE_FREE, '免费')
