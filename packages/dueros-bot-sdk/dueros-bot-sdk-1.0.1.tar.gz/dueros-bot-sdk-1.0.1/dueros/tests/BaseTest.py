# encoding: utf8

import math
import logging
import unittest
import dueros.Log as log


class BaseTest(object):

    def test_sqrt(self):
        self.assertEqual(math.sqrt(4) * math.sqrt(4), 4)


if __name__ == "__main__":
    # unittest.main()
    # log.init_log("./log/my_program")  # 日志保存到./log/my_program.log和./log/my_program.log.wf，按天切割，保留7天
    # logging.info("Hello World!!!")
    a = 'dfsfd#123'
    print(a.split('#', 1)[0])
