from functools import wraps

from flask import Blueprint, request, jsonify, session

from models.Message import Message, MsgType
from models.User import User
from services.user_service import UserService

user_bp = Blueprint('user', __name__, url_prefix='/api/user')

user_service = UserService()

def clear_session():
    session.pop("userID", None)
    session.pop("username", None)
    session.pop("steamID", None)
    session.pop("email", None)

def set_session(user:User):
    if user is not None:
        session["userID"] = user.userID
        session["username"] = user.username
        session["steamID"] = user.steamID
        session["email"] = user.email
    else:
        clear_session()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'userID' not in session:
            return Message(MsgType.ERROR,"not logged in",login=False).to_dict()
        return f(*args, **kwargs)
    return decorated_function

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return Message(MsgType.MESSAGE,"no data")

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    msg,user = user_service.create_new_user(username,password,email)
    set_session(user)

    return msg.to_dict()

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return Message(MsgType.MESSAGE,"no data")

    email = data.get('email')
    password = data.get('password')

    msg,user = user_service.login(email,password)

    set_session(user)

    return msg.to_dict()

@user_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    clear_session()
    return Message(MsgType.SUCCESS,"success").to_dict()

@user_bp.route('/update', methods=['POST'])
@login_required
def update():
    data = request.get_json()
    if not data:
        return Message(MsgType.MESSAGE,"no data")
    userID = session.get('userID')
    msg,user = user_service.update(userID,**data)
    if user:
        set_session(user)
    return msg.to_dict()

@user_bp.route('/check_login', methods=['GET'])
@login_required
def check_login():
    user_info = {
        "is_login":True,
        "userID":session.get('userID'),
        "email":session.get('email'),
        "username":session.get('username'),
        "steamID":session.get('steamID')
    }
    return Message(MsgType.SUCCESS,"login",login=True,user_info=user_info).to_dict()