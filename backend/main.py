from flask import Flask
from flask_cors import CORS

import config.settings
from api.captcha_routes import captcha_routes
from api.user_routes import user_bp
from api.steam_login_routes import steam_login_bp
from api.verification_code_routes import verification_code_bp

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}},supports_credentials=True)

app.secret_key = config.settings.secret_key
app.register_blueprint(user_bp)

app.register_blueprint(steam_login_bp)

app.register_blueprint(captcha_routes)

app.register_blueprint(verification_code_bp)

@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=False)