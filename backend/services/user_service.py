from models.Message import Message
from models.User import Authority, User
from repositories.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def create_new_user(self,username:str,password:str,email:str) -> (Message,User):
        return self.repo.create_new_user(username,password,email)

    def create_new_admin(self,username:str,password:str,email:str) -> (Message,User):
        return self.repo.create_new_user(username,password,email,authority=Authority.ADMIN)

    def login(self,email:str,password:str) -> (Message,User):
        return self.repo.login(email,password)

    def update(self,userID:int, **kwargs) -> (Message,User):
        return self.repo.update_user(userID,**kwargs)