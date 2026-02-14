from flask import Blueprint,request

from models.Message import Message, MsgType
from services.code_service import VerificationCodeService

verification_code_bp = Blueprint('verification_code',__name__,url_prefix='/api/code')

verification_code_service = VerificationCodeService()

@verification_code_bp.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    if not data:
        return Message(MsgType.MESSAGE,"no data")

    email = data['email']
    msg,verification_code = verification_code_service.gen_new_code(email)
    print(msg.to_dict())
    return msg.to_dict()

@verification_code_bp.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    if not data:
        return Message(MsgType.MESSAGE,"no data")
    email = data['email']
    code = data['code']
    msg = verification_code_service.verify_code(email,code)
    return msg.to_dict()