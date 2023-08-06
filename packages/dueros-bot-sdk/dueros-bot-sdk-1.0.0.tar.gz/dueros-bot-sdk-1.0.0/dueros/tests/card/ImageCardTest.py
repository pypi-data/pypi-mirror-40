# encoding: utf8

import unittest
from dueros.card.ImageCard import ImageCard


class ImageCardTest(unittest.TestCase):

    '''
    图片卡片测试
    '''

    def setUp(self):
        self.card = ImageCard()

    def testAddItem(self):
        '''
        测试addItem方法
        :return:
        '''

        self.card.add_item('www.png')
        card = {
            'type': 'image',
            'list': [
                {'src':'www.png'}
            ]
        }
        self.assertEqual(self.card.get_data(), card)
        self.card.add_item('www.png', 'www.thumbnail');
        card = {
            'type': 'image',
            'list': [
                {'src': 'www.png'},
                {'src': 'www.png', 'thumbnail': 'www.thumbnail'}
            ]
        }
        self.assertEqual(self.card.get_data(), card)
