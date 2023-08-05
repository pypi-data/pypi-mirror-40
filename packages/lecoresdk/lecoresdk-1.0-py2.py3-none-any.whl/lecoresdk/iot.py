#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import json
import utils
import config
import base64
import fc_error
from . import fc


class IoTData(object):
    def __init__(self):
        self.fc = fc.Client()

    # {topic: "", payload: ""}
    def publish(self, params):
        params_var = params
        if ((not utils.check_param(params_var, "topic")) or
            (not utils.check_param(params_var, "payload"))):
            return fc_error.PY_RUNTIME_ERROR_INVAILD_PARAM
        
        if ((not isinstance(params_var["topic"], str)) or 
            (not isinstance(params_var["payload"], str))):
            return fc_error.PY_RUNTIME_ERROR_INVAILD_PARAM

        context = {"custom": {
                    "source": os.environ.get("FUNCTION_ID"),
                    "topic": params_var["topic"]}}
        context_str = json.dumps(context)
        context_bytes = base64.standard_b64encode(context_str.encode("utf-8"))
        invoker_context = context_bytes.decode("utf-8")
        invoke_params = {"functionId": os.environ.get("ROUTER_FUNCTION_ID"),
                         "invocationType": config.INVOCATION_TYPE_ASYNC,
                         "invokerContext": invoker_context,
                         "payload": params_var["payload"]}
        self.fc.invoke_function(invoke_params)
        return fc_error.PY_RUNTIME_SUCCESS

    # {productKey: "", deviceName: "", payload: ""}
    def getThingProperties(self, params):
        params_var = params
        if (("payload" not in params_var) or
            (not isinstance(params["payload"], list))):
            return fc_error.PY_RUNTIME_ERROR_INVAILD_PARAM
    
        parameters = {"productKey": params_var["productKey"],
                      "deviceName": params_var["deviceName"],
                      "service": 'get',
                      "payload": params_var["payload"]}
        ret = self.callThingService(parameters)
        return ret

    # {productKey: "", deviceName: "", payload: ""}
    def setThingProperties(self, params):
        params_var = params
        if not utils.check_param(params_var, "payload"):
            return fc_error.PY_RUNTIME_ERROR_INVAILD_PARAM
        if not isinstance(params["payload"], dict):
            return fc_error.PY_RUNTIME_ERROR_INVAILD_PARAM
        
        parameters = {"productKey": params_var["productKey"],
                      "deviceName": params_var["deviceName"],
                      "service": 'set',
                      "payload": params_var["payload"]}
        ret = self.callThingService(parameters)
        return ret

    # {productKey: "", deviceName: "", service:"", payload: ""}
    def callThingService(self, params):
        params_var = params
        if ((not utils.check_param(params_var, "productKey")) or
            (not utils.check_param(params_var, "deviceName")) or
            (not utils.check_param(params_var, "service"))):
            return fc_error.PY_RUNTIME_ERROR_INVAILD_PARAM

        if (("payload" not in params_var) or
            (not isinstance(params_var["productKey"], str)) or 
            (not isinstance(params_var["deviceName"], str)) or
            (not isinstance(params_var["service"], str))):
            return fc_error.PY_RUNTIME_ERROR_INVAILD_PARAM

        if ((params_var["service"] != "get") and 
            (not isinstance(params["payload"], dict))):
            return fc_error.PY_RUNTIME_ERROR_INVAILD_PARAM
        
        topic = "/sys/things/{0}/{1}/services/{2}".format(params_var["productKey"], params_var["deviceName"],
                                                        params_var["service"])
        context = {"custom": {"topic": topic}}
        context_str = json.dumps(context)
        context_bytes = base64.standard_b64encode(context_str.encode("utf-8"))
        invoker_context = context_bytes.decode("utf-8")
        invokeParams = {"functionId": os.environ.get("THING_FUNCTION_ID"),
                        "invocationType": config.INVOCATION_TYPE_SYNC,
                        "invokerContext": invoker_context,
                        "payload": json.dumps(params_var["payload"])}
        ret = self.fc.invoke_function(invokeParams)
        if ret is not None and "payload" in ret:
            value = base64.b64decode(ret["payload"]).decode("utf-8")
            statusCode = ret["statusCode"]
            if statusCode == 200:
                return json.loads(value)
            else:
                raise fc_error.RequestException(msg=value)

    def getThingsWithTags(self, params):
        params_var = params
        if (("payload" not in params_var) or
            (not isinstance(params["payload"], list))):
            return fc_error.PY_RUNTIME_ERROR_INVAILD_PARAM
        
        topic = "/sys/things///services/getthingswithtags"
        context = {"custom": {"topic": topic}}
        context_str = json.dumps(context)
        context_bytes = base64.standard_b64encode(context_str.encode("utf-8"))
        invoker_context = context_bytes.decode("utf-8")
        invokeParams = {"functionId": os.environ.get("THING_FUNCTION_ID"),
                        "invocationType": config.INVOCATION_TYPE_SYNC,
                        "invokerContext": invoker_context,
                        "payload": json.dumps(params["payload"])}
        ret = self.fc.invoke_function(invokeParams)
        if ret is not None and "payload" in ret:
            value = base64.b64decode(ret["payload"]).decode("utf-8")
            statusCode = ret["statusCode"]
            if statusCode == 200:
                return json.loads(value)
            else:
                raise fc_error.RequestException(msg=value)

if __name__ == '__main__':
    iot = IoTData()
