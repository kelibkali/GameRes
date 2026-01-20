from flask import Blueprint, session, request

from models.Message import Message, MsgType
from utils.captcha_utils import gen_random_string,create_img

captcha_routes = Blueprint('captcha_routes', __name__,url_prefix="/api/captcha")

@captcha_routes.route('/get', methods=['GET'])
def get_captcha():
    captcha = gen_random_string(4)
    session['captcha'] = captcha.upper()

    img = create_img(captcha)
    from flask import Response
    return Response(img, mimetype='image/png')

@captcha_routes.route('/verify', methods=['POST'])
def verify_captcha():
    data = request.get_json()
    user_input = data.get("captcha").strip().upper()

    stored_captcha  = session.get('captcha')

    if not stored_captcha:
        return Message(MsgType.MESSAGE,"验证码已过期")

    if user_input == stored_captcha:
        session.pop('captcha')
        return Message(MsgType.SUCCESS,"验证成功")
    else:
        return Message(MsgType.ERROR,"验证失败")