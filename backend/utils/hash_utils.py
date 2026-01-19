import bcrypt


def hash_with_salt(s_bytes: bytes):
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(s_bytes, salt)
    return hashed

def check_password(receive:str, password:bytes)->bool:
    return bcrypt.checkpw(receive.encode("utf-8"), password)