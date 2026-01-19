from random import randint

from peewee import IntegrityError

from models.Message import Message, MsgType
from models.User import User, Authority


class UserRepository:

    @staticmethod
    def generate_ramdom_id():
        min_id = int(1e5)
        max_id = int(1e9)
        return randint(min_id, max_id)

    @staticmethod
    def create_new_user(username:str,password:str,email:str,authority=Authority.USER.value) -> Message:
        # 最多尝试10次
        cnt = 10
        while cnt > 0:
            uid = UserRepository.generate_ramdom_id()
            try:
                User.create(
                    username=username,
                    password=password,
                    email=email,
                    userID=uid,
                    authority=authority,
                )
                return Message(msg_type=MsgType.SUCCESS,message= "创建用户成功。",userID=uid)
            except IntegrityError as e:
                print(e)
                cnt -= 1
                continue
        return Message(msg_type=MsgType.ERROR,message= "创建用户失败，请重新尝试。")

    @staticmethod
    def login(userID:int,password:str) -> Message:
        try:
            user:User = User.get(User.userID == userID)
        except Exception as e:
            return Message(msg_type=MsgType.ERROR,message= "用户不存在。")
        if user.check_password(password):
            return Message(msg_type=MsgType.ERROR,message= "密码错误。")
        return Message(msg_type=MsgType.MESSAGE,message= "登录成功。")
