# encoding: utf8

from dueros.directive.Display.tag.BaseTag import BaseTag
from dueros.directive.Display.tag.TagTypeEnum import TagTypeEnum


class AuditionTag(BaseTag):

    def __init__(self):
        super(AuditionTag, self).__init__(TagTypeEnum.TAG_TYPE_AUDITION_NEW, '试听')
