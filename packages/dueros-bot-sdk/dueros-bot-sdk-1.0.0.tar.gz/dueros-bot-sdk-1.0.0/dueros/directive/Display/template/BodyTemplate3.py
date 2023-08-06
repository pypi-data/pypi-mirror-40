# encoding: utf8
"""
BodyTemplate3模板
详见文档：https://dueros.baidu.com/didp/doc/dueros-bot-platform/dbp-custom/display-template_markdown#BodyTemplate3
"""

from dueros.directive.Display.template.TextImageTemplate import TextImageTemplate


class BodyTemplate3(TextImageTemplate):

    def __init__(self):
        super(BodyTemplate3, self).__init__('BodyTemplate3')
