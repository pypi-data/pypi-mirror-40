# encoding: utf8
from dueros.directive.BaseDirective import BaseDirective
from dueros.directive.Display.template.BaseTemplate import BaseTemplate


class RenderTemplate(BaseDirective):

    def __init__(self, base_template=''):
        super(RenderTemplate, self).__init__('Display.RenderTemplate')
        self.set_template(base_template)

    def set_template(self, template):
        """
        设置模板
        :param template:
        :return:
        """
        if isinstance(template, BaseTemplate):
            self.data['template'] = template.get_data()
