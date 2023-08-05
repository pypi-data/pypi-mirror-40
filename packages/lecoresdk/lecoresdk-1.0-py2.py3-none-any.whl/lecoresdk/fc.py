#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import config
import sync
import fc_error
import utils
import ipc_wrapper
import logging
import json


# {functionName: "functionid", invocaionType: "Sync or Async.", payload: ""}
class Client(object):
    def __init__(self):
        self.ipc = ipc_wrapper.ipc
        self.invokeSync = sync.SyncMsg_Event()

    def _getInvokeResult_cb(self, status, data):
        syncMsg = {}
        syncMsg["state"] = False
        syncMsg["msg"] = None
        try:
            if status == "success":
                logging.debug("staus:%s", status)
                syncMsg["state"] = True
                syncMsg["msg"] = data
            else:
                syncMsg["msg"] = ''
                syncMsg["state"] = False
        except:
            syncMsg["msg"] = ''
            syncMsg["state"] = False
        self.invokeSync.set(syncMsg)

    def invoke_function(self, params):
        logging.debug("%%%%%%start%%%%%%%%")
        params_var = params
        if ((not utils.check_param(params_var, "invokerContext")) or
            ("payload" not in params_var)):
            logging.error("invalid param1")
            return fc_error.PY_RUNTIME_ERROR_INVAILD_PARAM

        if "invocationType" not in params_var:
            invocationType = config.INVOCATION_TYPE_SYNC
        else:
            invocationType = params["invocationType"]
        if not (invocationType == config.INVOCATION_TYPE_ASYNC or 
            invocationType == config.INVOCATION_TYPE_SYNC):
            logging.error("invalid param2")
            return fc_error.PY_RUNTIME_ERROR_INVAILD_PARAM

        if (not utils.check_param(params_var, "functionId")):
            if ((not utils.check_param(params_var, "serviceName")) or
                (not utils.check_param(params_var, "functionName")) or
                (not isinstance(params_var["serviceName"], str)) or
                (not isinstance(params_var["functionName"], str))):
                logging.error("invalid param3")
                return fc_error.PY_RUNTIME_ERROR_INVAILD_PARAM
            serviceName = params_var["serviceName"]
            functionName = params_var["functionName"]
            functionId = utils.buildArnString('', '', serviceName, functionName)
        else:
            functionId = params_var["functionId"]

        if ((not isinstance(params_var["invokerContext"], str)) or 
            (not isinstance(functionId, str)) or
            (not (isinstance(params_var["payload"], str) or
            isinstance(params_var["payload"], bytes)))):
            logging.error("invalid param4")
            return fc_error.PY_RUNTIME_ERROR_INVAILD_PARAM

        invokerContext = params["invokerContext"]
        payload = params["payload"]
        msg = self.ipc.invokeTask(functionId, invokerContext, invocationType, payload)
        if invocationType == config.INVOCATION_TYPE_ASYNC:
            if ((msg is not None) and 
                ("msg" in msg)):
                ret = msg["msg"]
                if (("statusCode" in ret) and 
                    (ret["statusCode"] == 202) and 
                    ("headers" in ret)):
                    header = ret["headers"]
                    invocationId = header[config.HEADER_INVOCATION_ID]
                    logging.debug("%%%%%%Done%%%%%%%")
                    logging.debug(invocationId)
                    return invocationId
            raise fc_error.RequestException(msg="call async function fail")
        else:
            if ((msg is not None) and 
                ("msg" in msg) and 
                ("headers" in msg["msg"]) and 
                (config.HEADER_INVOCATION_ID in msg["msg"]["headers"])):
                header = msg["msg"]["headers"]        
                invocationId = header[config.HEADER_INVOCATION_ID]
                logging.debug("getTaskResult start:%s", invocationId)
                syncMsg = self.ipc.getTaskResult(functionId, invocationId)
                if (None == syncMsg):
                    logging.error("getTaskResult timeout")
                    raise fc_error.WSConnException(msg="get task result timeout")
                ret = None
                if "msg" in syncMsg:
                    ret = syncMsg["msg"]
                    if "body" in ret:
                        body = ret["body"]
                    else:
                        body = ""
                    if "headers" in ret and config.HEADER_FUNCTION_ERROR in ret["headers"]:
                        functionErr = ret["headers"][config.HEADER_FUNCTION_ERROR]
                    else:
                        functionErr = ""
                    result = {
                        "statusCode": ret["statusCode"],
                        "functionError": functionErr,
                        "payload": body}
                    logging.debug("getTaskResult done:%s", ret)
                    logging.debug("%%%%%%Done%%%%%%%%")
                    return result
                else:
                    logging.error("getTaskResult error")
                    return None
            else:
                logging.error("invokeTask timeout")
                return None

