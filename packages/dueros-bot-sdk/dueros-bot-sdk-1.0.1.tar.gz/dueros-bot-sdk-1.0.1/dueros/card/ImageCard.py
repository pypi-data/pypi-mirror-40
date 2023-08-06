# encoding: utf8
"""
图片卡片
详见文档：https://dueros.baidu.com/didp/doc/dueros-bot-platform/dbp-custom/cards_markdown#%E5%9B%BE%E7%89%87%E5%8D%A1%E7%89%87
"""

from dueros.card.BaseCard import BaseCard


class ImageCard(BaseCard):

    def __init__(self):
        super(ImageCard, self).__init__()
        self.data['type'] = 'image'

    def add_item(self, src, thumbnail=''):
        """
        添加
        :param src:
        :param thumbnail:
        :return:
        """

        if not src:
            return self

        if not 'list' in self.data:
            self.data['list'] = []

        item = {}
        item['src'] = src

        if thumbnail:
            item['thumbnail'] = thumbnail
        self.data['list'].append(item)
        return self
