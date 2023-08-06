# encoding: utf8

"""
BodyTemplate4模板
详见文档：https://dueros.baidu.com/didp/doc/dueros-bot-platform/dbp-custom/display-template_markdown#BodyTemplate4
"""

from dueros.directive.Display.template.TextImageTemplate import TextImageTemplate


class BodyTemplate4(TextImageTemplate):

    def __init__(self):
        super(BodyTemplate4, self).__init__('BodyTemplate4')
