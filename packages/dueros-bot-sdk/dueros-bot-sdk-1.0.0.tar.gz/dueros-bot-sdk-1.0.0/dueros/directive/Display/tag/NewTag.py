# encoding: utf8

from dueros.directive.Display.tag.TagTypeEnum import TagTypeEnum
from dueros.directive.Display.tag.BaseTag import BaseTag


class NewTag(BaseTag):

    def __init__(self):
        super(NewTag, self).__init__(TagTypeEnum.TAG_TYPE_NEW, '最新')
