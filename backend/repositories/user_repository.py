from random import randint

from peewee import IntegrityError, DoesNotExist

from models.Message import Message, MsgType
from models.User import User, Authority
from utils.hash_utils import hash_with_salt


class UserRepository:

    @staticmethod
    def generate_ramdom_id():
        min_id = int(1e5)
        max_id = int(1e9)
        return randint(min_id, max_id)

    @staticmethod
    def create_new_user(username:str,password:str,email:str,authority=Authority.USER.value) -> (Message,User):

        user = User.get_or_none(User.email == email)
        if user is not None:
            return Message(msg_type=MsgType.ERROR,message="邮箱已被使用过"),None

        # 最多尝试10次
        cnt = 10
        while cnt > 0:
            uid = UserRepository.generate_ramdom_id()
            try:
                user = User.create(
                    username=username,
                    password=password,
                    email=email,
                    userID=uid,
                    authority=authority,
                )
                return Message(msg_type=MsgType.SUCCESS,message= "注册成功",userID=uid),user
            except IntegrityError as e:
                print(e)
                cnt -= 1
                continue
        return Message(msg_type=MsgType.ERROR, message="注册失败"),None

    @staticmethod
    def login(userID:int,password:str) -> (Message,User):
        try:
            user:User = User.get(User.userID == userID)
        except Exception as e:
            return Message(msg_type=MsgType.ERROR,message= "用户不存在。"),None
        if user.check_password(password):
            return Message(msg_type=MsgType.ERROR,message= "密码错误。"),None
        return Message(msg_type=MsgType.MESSAGE,message= "登录成功。"),user
    
    @staticmethod
    def update_user(userID:int,**kwargs) -> (Message,User):
        try:
            user = User.get(User.userID == userID)

            for k,v in kwargs.items():
                if k == "userID" or k == "authority":
                    continue

                if k == "password":
                    user.password_hash = hash_with_salt(v.encode("utf8"))
                else:
                    setattr(user, k, v)

            user.save()
        except Exception as e:
            return Message(msg_type=MsgType.ERROR,message="更新失败。"),None
        return Message(msg_type=MsgType.SUCCESS,message="更新成功"),user

