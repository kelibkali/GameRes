import random

from models.Message import Message, MsgType
from models.VerificationCode import VerificationCode, CodeStatus


class CodeRepository:

    @staticmethod
    def gen_random_code():
        return f"{random.randint(0, 999999):06d}"

    @staticmethod
    def gen_new_code(email:str):
        try:
            code = CodeRepository.gen_random_code()
            verification_code:VerificationCode = VerificationCode.create(
                email=email,
                code=code,
            )
        except Exception as e:
            return Message(msg_type=MsgType.ERROR, message=f"{e}")
        return Message(msg_type=MsgType.SUCCESS, message=code),verification_code

    @staticmethod
    def verify_code(email:str, code:str):
        try:
            this_code:VerificationCode = VerificationCode.get(
               (VerificationCode.email == email) &
                (VerificationCode.status == CodeStatus.PENDING.value)
            )

            if this_code.is_expired():
                this_code.status = CodeStatus.EXPIRED.value
                this_code.save()
                return Message(msg_type=MsgType.MESSAGE, message=f"验证码已过期。")

            if this_code.code == code:
                this_code.status = CodeStatus.USED.value
                this_code.save()
                return Message(msg_type=MsgType.SUCCESS,message="验证成功！")
        except Exception as e:
            return Message(msg_type=MsgType.ERROR, message=f"{e}")