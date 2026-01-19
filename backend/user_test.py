import database
from models.User import User
from database.connection import db_inst

db_inst.create_tables([User])
try:
    new_u = User.create(
        username="kali",
        userID=12345,
        email="example@email.com",
        password="123456"
    )
    print(f"用户 {new_u.username} 创建成功！")
    print(f"存储的哈希值 (bytes): {new_u.password_hash}")
except Exception as e:
    print(e)

# 登录验证示例
user_to_check = User.get(User.username == "kali")

input_password = "123456"
if user_to_check.check_password(input_password):
    print("登录成功！")
else:
    print("登录失败，密码错误！")

input_wrong_password = "wrong_password"
if not user_to_check.check_password(input_wrong_password):
    print("登录失败，密码错误！（预期行为）")
else:
    print("登录成功！（意外行为）")

print("\n用户信息:", user_to_check.to_dict())
