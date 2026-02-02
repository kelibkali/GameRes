from urllib.parse import urlencode

import requests
from flask import Blueprint, request, redirect,session

from api.user_routes import login_required,user_service

from config.settings import (front_url)
from models.Message import Message, MsgType

steam_login_bp = Blueprint('steam_login',__name__,url_prefix="/api/steam")

STEAM_OPENID_LOGIN_URL = "https://steamcommunity.com/openid/login"
RETURN_TO = 'http://localhost:5000/api/steam/callback'

@steam_login_bp.route('/login')
@login_required
def login_steam():
    # 构建连接并重定向 使用/callback接收回调
    params = {
        'openid.ns': 'http://specs.openid.net/auth/2.0',
        'openid.mode': 'checkid_setup',
        'openid.return_to': RETURN_TO,
        'openid.realm': request.url_root,
        'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select'
    }
    return redirect(f"{STEAM_OPENID_LOGIN_URL}?{urlencode(params)}")

@steam_login_bp.route('/callback')
def callback():
    args = request.args

    # 错误处理
    if args.get("openid.mode") == "error":
        error_msg = args.get("openid.error", "Unknown error occurred during Steam authentication.")
        print(error_msg)
        return redirect(f"{front_url}?auth_error=true")

    required = ['openid.mode', 'openid.return_to', 'openid.identity', 'openid.claimed_id']
    if not all(k in args for k in required):
        return Message(MsgType.MESSAGE,"缺少必要参数").to_dict()

    if args['openid.mode'] != 'id_res':
        return Message(MsgType.MESSAGE,"无效的认证模式").to_dict()

    verify_data = dict(args.items())
    verify_data['openid.mode'] = "check_authentication"

    resp = requests.post(STEAM_OPENID_LOGIN_URL,data = verify_data)

    if resp.status_code != 200:
        return Message(MsgType.ERROR,"服务器错误").to_dict()

    if "is_valid:true" in resp.text:
        claimed_id = args['openid.claimed_id']
        steamID = claimed_id.split('/')[-1]
        session['steamID'] = steamID

        user_service.update(session['userID'],steamID=steamID)

        # 认证成功后 重定向到前端应用
        return redirect(front_url)
    else:
        return redirect('http://localhost:5173?auth_error=true')

@steam_login_bp.route('/has_steamid')
def has_steamid():
    steamID = session.get('steamID')
    if steamID and steamID != "":
        return Message(MsgType.SUCCESS,"success",steamID=steamID)
    else:
        return Message(MsgType.MESSAGE,"未登录").to_dict()

@steam_login_bp.route('/logout')
def logout():
    session.pop("steamID", None)
    user_service.update(session['userID'], steamID="")
    return Message(MsgType.SUCCESS, "登出成功").to_dict()