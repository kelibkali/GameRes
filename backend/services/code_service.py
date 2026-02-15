from models.Message import Message
from models.User import User
from models.VerificationCode import VerificationCode
from repositories.code_repository import CodeRepository


class VerificationCodeService:
    def __init__(self):
        self.repo = CodeRepository()

    def gen_new_code(self,email:str) -> tuple[Message,VerificationCode]:
        return self.repo.gen_new_code(email)

    def verify_code(self,email:str,code:str) -> Message:
        return self.repo.verify_code(email,code)