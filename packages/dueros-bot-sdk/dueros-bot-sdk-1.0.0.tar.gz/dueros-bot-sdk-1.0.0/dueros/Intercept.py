# encoding: utf8

class Intercept:

    def preprocess(self, bot):
        '''

        :param bot:
        :return:
        如果返回非null，跳过后面addHandler，addEventListener添加的回调
        '''
        pass

    def postprocess(self, bot, result):
        '''
        在调用response->build 之前统一对handler的输出结果进行修改
        :param bot:
        :param result:  []
        :return:[]
        '''

        return result
