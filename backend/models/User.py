from enum import Enum
from typing import cast

from peewee import CharField, IntegerField, Model, BlobField

from database.connection import db_inst
from utils.hash_utils import hash_with_salt,check_password


class Status(Enum):
    ENABLED = 0
    DISABLED = 1

class Authority(Enum):
    ADMIN = "admin"
    USER = "user"

class User(Model):
    class Meta:
        database = db_inst
        table_name = "users"

    userID = IntegerField(unique=True, primary_key=True)
    username = CharField(unique=False,max_length=40)
    password_hash = BlobField(unique=False)  # 存储bytes类型的哈希值
    email = CharField(unique=True,default="",max_length=50)
    steamID = CharField(unique=False,default="",max_length=50) # steamID 唯一
    authority = CharField(unique=False,default=Authority.USER.value,max_length=10)
    status = IntegerField(default=Status.ENABLED.value)

    filePath = ""

    @classmethod
    def create(cls,**query):
        password = query.pop("password")
        password_hash_bytes = hash_with_salt(password.encode("utf8"))

        instance = cls(**query)
        instance.password_hash = password_hash_bytes
        query["password_hash"] = password_hash_bytes
        return super().create(**query)

    def is_admin(self):
        return self.authority == Authority.ADMIN.value

    def is_user(self):
        return self.authority == Authority.USER.value

    def check_password(self, receive:str)->bool:
        return check_password(receive, cast(bytes,self.password_hash))

    def to_dict(self):
        return {
            "username": self.username,
            "userID": self.userID,
            "steamID": self.steamID,
            "filePath": self.filePath,
            "email": self.email,
            "status": self.status,
            "authority": self.authority,
        }