# encoding: utf8
"""
    第三方账号授权
    debug模式：要将回调地址域名替换下 https://xiaodu-dbp.baidu.com/xxxx
"""

from dueros.card.BaseCard import BaseCard


class LinkAccountCard(BaseCard):

    def __init__(self):
        super(LinkAccountCard, self).__init__()
        self.data['type'] = 'LinkAccount'
