# encoding: utf8


class BotMonitorConfig:

    @staticmethod
    def getHost():
        return 'dueros-api.baidu.com'

    @staticmethod
    def get_upload_url():
        return 'https://dueros-api.baidu.com/uploadmonitordata'

    @staticmethod
    def get_sdk_version():
        return '2.0.0'

    @staticmethod
    def get_sdk_type():
        return 'python'

    @staticmethod
    def get_upload_port():
        return 443

    @staticmethod
    def get_upload_path():
        return '/uploadmonitordata'
