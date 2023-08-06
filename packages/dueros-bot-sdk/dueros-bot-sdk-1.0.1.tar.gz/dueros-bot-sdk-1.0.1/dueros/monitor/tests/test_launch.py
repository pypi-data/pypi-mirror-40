# encoding: utf8
import os
import json
from dueros.monitor.model.Request import Request


class test_launch:
    pass


if __name__ == '__main__':

    def requestData():
        with open("../data/test_launch.json", 'r', encoding='utf-8') as load_f:
            return load_f.read()
    requestData = requestData()
    # print(requestData)

    request = Request(json.loads(requestData))
    print(request.get_type())
    print(request.get_user_id())
    print(request.get_bot_id())
    print(request.is_dialog_state_completed())
