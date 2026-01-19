from models.Message import Message
from models.User import Authority
from repositories.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def create_new_user(self,username:str,password:str,email:str) -> Message:
        return self.repo.create_new_user(username,password,email)

    def create_new_admin(self,username:str,password:str,email:str) -> Message:
        return self.repo.create_new_user(username,password,email,authority=Authority.ADMIN)

    def login(self,userID:int,password:str) -> Message:
        return self.repo.login(userID,password)