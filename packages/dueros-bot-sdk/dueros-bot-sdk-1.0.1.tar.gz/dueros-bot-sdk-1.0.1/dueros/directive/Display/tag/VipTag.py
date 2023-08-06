# encoding: utf8

from dueros.directive.Display.tag.BaseTag import BaseTag
from dueros.directive.Display.tag.TagTypeEnum import TagTypeEnum


class VipTag(BaseTag):

    def __init__(self):
        super(VipTag, self).__init__(TagTypeEnum.TAG_TYPE_VIP, 'VIP')
