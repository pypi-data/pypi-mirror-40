# encoding: utf8

from dueros.card.BaseCard import BaseCard


class ListCardItem(BaseCard):

    def __init__(self):
        super(ListCardItem, self).__init__(['title', 'content', 'url', 'image'])
