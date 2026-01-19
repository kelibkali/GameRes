from flask import Flask
from api.user_routes import user_bp
app = Flask(__name__)

app.register_blueprint(user_bp)

@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)