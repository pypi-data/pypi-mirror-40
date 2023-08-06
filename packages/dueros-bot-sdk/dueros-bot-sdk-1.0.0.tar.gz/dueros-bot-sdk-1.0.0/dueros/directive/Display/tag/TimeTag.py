# encoding: utf8

from dueros.directive.Display.tag.BaseTag import BaseTag
from dueros.directive.Display.tag.TagTypeEnum import TagTypeEnum


class TimeTag(BaseTag):

    def __init__(self, time):
        super(TimeTag, self).__init__(TagTypeEnum.TAG_TYPE_TIME, time)
