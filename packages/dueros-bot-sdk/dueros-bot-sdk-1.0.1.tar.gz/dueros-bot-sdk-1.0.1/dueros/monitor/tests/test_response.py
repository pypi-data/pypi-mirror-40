# encoding: utf8
import os
import json
from dueros.monitor.model.Response import Response


class test_response:
    pass


if __name__ == '__main__':

    def responseData():
        with open("../data/test_response_tax.json", 'r', encoding='utf-8') as load_f:
            return load_f.read()
    responseData = responseData()
    # print(responseData)

    response = Response(json.loads(responseData))

    print(response.get_slot_name())
    print(response.get_should_end_session())
    print(response.get_output_speech())
    print(response.get_reprompt())
