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
        code=200
        response_data["message"] = self.message
        response_data["type"] = self.msg_type.value

        for attr,value in self.__dict__.items():
            if attr != "msg_type" and attr != "message":
                response_data[attr] = value
        return jsonify(response_data), code