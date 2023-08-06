# encoding: utf8
from dueros.directive.BaseDirective import BaseDirective


class LaunchBrowser(BaseDirective):
    """
        用于调用浏览器指令的类
    """

    def __init__(self, url):

        super(LaunchBrowser, self).__init__('WebBrowser.LaunchBrowser')
        self.data['url'] = url
        self.data['token'] = self.gen_token()
