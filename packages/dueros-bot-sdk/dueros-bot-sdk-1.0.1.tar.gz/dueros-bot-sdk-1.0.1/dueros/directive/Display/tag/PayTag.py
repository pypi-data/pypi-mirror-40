# encoding: utf8

from dueros.directive.Display.tag.BaseTag import BaseTag
from dueros.directive.Display.tag.TagTypeEnum import TagTypeEnum


class PayTag(BaseTag):

    def __init__(self):
        super(PayTag, self).__init__(TagTypeEnum.TAG_TYPE_PAY, '付费')
