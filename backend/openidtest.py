from flask import Flask, request, redirect, session, jsonify
import requests
from urllib.parse import urlencode
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'kali'
CORS(app, supports_credentials=True)  # 允许跨域请求携带凭证

STEAM_LOGIN_URL = 'https://steamcommunity.com/openid/login'
RETURN_TO = 'http://localhost:5000/callback'

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

    # --- 错误处理 ---
    # 检查是否有错误参数
    if args.get('openid.mode') == 'error':
        error_msg = args.get('openid.error', 'Unknown error occurred during Steam authentication.')
        print(f"Steam returned an error: {error_msg}")
        return redirect('http://localhost:5173?auth_error=true')

    required = ['openid.mode', 'openid.return_to', 'openid.identity', 'openid.claimed_id']
    if not all(k in args for k in required):
        return "认证失败：缺少必要参数", 400

    if args['openid.mode'] != 'id_res':
        return "认证失败：无效的认证模式", 400

    verify_data = dict(args.items())
    verify_data['openid.mode'] = 'check_authentication'

    resp = requests.post(STEAM_LOGIN_URL, data=verify_data)

    if resp.status_code != 200:
        return "认证失败：服务器错误", 500

    if 'is_valid:true' in resp.text:
        claimed_id = args['openid.claimed_id']
        steam_id = claimed_id.split('/')[-1]
        session['steam_id'] = steam_id

        # 认证成功后，重定向到前端应用
        # 你可以在这里传递一些信息，比如在URL参数中
        # 例如: http://localhost:5173?login_success=true
        return redirect('http://localhost:5173')
    else:
        # 验证失败
        print("Steam verification failed.")
        return redirect('http://localhost:5173?auth_error=true') # 重定向到前端错误页


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('steam_id', None)
    return jsonify({'success': True})


@app.route('/api/user')
def get_user():
    steam_id = session.get('steam_id')
    if steam_id:
        return jsonify({'steam_id': steam_id}), 200
    else:
        return jsonify({'error': '未登录'}), 401


if __name__ == '__main__':
    app.run(debug=True, port=5000)