# encoding: utf8
import os
import json
from dueros.monitor.model.Request import Request


class test_request:
    pass


if __name__ == '__main__':

    def requestData():
        with open("../data/intent_request_tax.json", 'r', encoding='utf-8') as load_f:
            return load_f.read()
    requestData = requestData()

    request = Request(json.loads(requestData))

    print(request.get_type())
    print(request.get_user_id())
    print(request.get_query())
    print(request.get_bot_id())
    print(request.get_request_id())
    print(request.get_reson())
    print(request.get_intent_name())
    print(request.get_session_id())
    print(request.get_device_id())
    print(request.get_location())
    print(request.is_dialog_state_completed())
