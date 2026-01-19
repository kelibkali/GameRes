from flask import Flask, request, redirect, session, url_for
import requests
from urllib.parse import urlencode

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 必需的密钥 加密session

# Steam OpenID 配置
STEAM_LOGIN_URL = 'https://steamcommunity.com/openid/login'
RETURN_TO = 'http://127.0.0.1:5000/callback'


@app.route('/')
def index():
    steam_id = session.get('steam_id')
    if steam_id:
        return f"<h1>欢迎, SteamID: {steam_id}!</h1><br><a href='/logout'>退出登录</a>"
    else:
        return "<h1>欢迎!</h1><br><a href='/login'>使用Steam登录</a>"


@app.route('/login')
def login():
    params = {
        'openid.ns': 'http://specs.openid.net/auth/2.0',
        'openid.mode': 'checkid_setup',
        'openid.return_to': RETURN_TO,
        'openid.realm': request.url_root,
        'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select'
    }
    return redirect(f"{STEAM_LOGIN_URL}?{urlencode(params)}")


@app.route('/callback')
def callback():
    args = request.args

    # 验证必需参数
    required = ['openid.mode', 'openid.return_to', 'openid.identity', 'openid.claimed_id']
    if not all(k in args for k in required):
        return "认证失败：缺少必要参数", 400

    if args['openid.mode'] != 'id_res':
        return "认证失败：无效的认证模式", 400

    # 验证请求
    verify_data = dict(args.items())
    verify_data['openid.mode'] = 'check_authentication'

    resp = requests.post(STEAM_LOGIN_URL, data=verify_data)

    if resp.status_code != 200:
        return "认证失败：服务器错误", 500

    if 'is_valid:true' in resp.text:
        # 提取SteamID
        claimed_id = args['openid.claimed_id']
        steam_id = claimed_id.split('/')[-1]

        session['steam_id'] = steam_id
        return redirect(url_for('index'))
    else:
        return "认证失败：验证不通过", 400


@app.route('/logout')
def logout():
    session.pop('steam_id', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)