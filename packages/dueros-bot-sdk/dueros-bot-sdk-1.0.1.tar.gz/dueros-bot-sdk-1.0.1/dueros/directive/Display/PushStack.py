# encoding: utf8

"""
用于生成PushStack指令的类
"""

from dueros.directive.BaseDirective import BaseDirective


class PushStack(BaseDirective):

    def __init__(self):
        super(PushStack, self).__init__('Display.PushStack')
