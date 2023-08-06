# encoding: utf8

from dueros.directive.Display.tag.BaseTag import BaseTag
from dueros.directive.Display.tag.TagTypeEnum import TagTypeEnum


class AmountTag(BaseTag):

    def __init__(self, amount):
        super(AmountTag, self).__init__(TagTypeEnum.TAG_TYPE_AMOUNT, amount)
