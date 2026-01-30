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

def set_session(user:User):
    if user is not None:
        session["userID"] = user.userID
        session["username"] = user.username
        session["steamID"] = user.steamID
    else:
        clear_session()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'userID' not in session:
            return Message(MsgType.ERROR,"not logged in")
        return f(*args, **kwargs)
    return decorated_function

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return Message(MsgType.MESSAGE,"no data")

    username = data.get('username')
    password = data.get('password')
    email = data.get('send_email')

    msg,user = user_service.create_new_user(username,password,email)
    set_session(user)

    return msg.to_dict()

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return Message(MsgType.MESSAGE,"no data")

    userID = data.get('userID')
    password = data.get('password')

    msg,user = user_service.login(userID,password)

    set_session(user)

    return msg.to_dict()

@user_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    clear_session()
    return Message(MsgType.SUCCESS,"success")

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