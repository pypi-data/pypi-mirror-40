# encoding: utf8

from dueros.directive.Display.tag.BaseTag import BaseTag
from dueros.directive.Display.tag.TagTypeEnum import TagTypeEnum


class CustomTag(BaseTag):

    def __init__(self, text):
        super(CustomTag, self).__init__(TagTypeEnum.TAG_TYPE_CUSTOM, text)
