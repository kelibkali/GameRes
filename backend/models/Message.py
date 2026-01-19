from enum import Enum

from flask import jsonify, Response


class MsgType(Enum):
    ERROR = "error"
    SUCCESS = "success"
    MESSAGE = "message"

class Message:
    def __init__(self,msg_type:MsgType,message:str,**kwargs):
        self.msg_type = msg_type
        self.message = message

        for k,v in kwargs.items():
            setattr(self,k,v)


    def to_dict(self) -> tuple[Response, int]:

        response_data = {}

        if self.msg_type == MsgType.ERROR:
            response_data["error"] = self.message
            code = 500
        elif self.msg_type == MsgType.SUCCESS:
            response_data["success"] = self.message
            code = 200
        else:
            response_data["message"] = self.message
            code = 400

        for attr,value in self.__dict__.items():
            if attr != "msg_type" and attr != "message":
                response_data[attr] = value

        return jsonify(response_data), code