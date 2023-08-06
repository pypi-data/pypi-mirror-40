# encoding: utf8
import unittest
from dueros.card.TextCard import TextCard


class TextCardTest(unittest.TestCase):
    '''
    TextCard单元测试
    '''

    def setUp(self):
        self.card = TextCard('这是TextCard')

    def testAddCueWords(self):
        '''
        测试添加关键字
        :return:
        '''
        self.card.add_cue_words(['cuewords1', 'cuewords2'])
        card = {
            'type': 'txt',
            'content': '这是TextCard',
            'cueWords': ['cuewords1', 'cuewords2']
        }
        self.assertEqual(self.card.get_data(), card)

    def testSetAnchor(self):
        '''
        测试setAnchor方法
        :return:
        '''
        self.card.set_anchor('http://www.baidu.com', '百度')
        card = {
            'type': 'txt',
            'content': '这是TextCard',
            'url': 'http://www.baidu.com',
            'anchorText': '百度'
        }
        self.assertEqual(self.card.get_data(), card)

    def testGetData(self):
        '''
        测试getData方法
        :return:
        '''
        card = {
            'type': 'txt',
            'content': '这是TextCard',
        }
        self.assertEqual(self.card.get_data(), card)

    pass
