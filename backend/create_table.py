from database.connection import db_inst
from models.User import User
from models.VerificationCode import VerificationCode

db_inst.create_tables([User, VerificationCode])