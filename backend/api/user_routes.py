from flask import Blueprint,request,jsonify

from services.user_service import UserService

user_bp = Blueprint('user', __name__, url_prefix='/api/user')

user_service = UserService()

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    msg = user_service.create_new_user(username,password,email)
    return msg.to_dict()

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    userID = data.get('userID')
    password = data.get('password')

    msg = user_service.login(userID,password)
    return msg.to_dict()