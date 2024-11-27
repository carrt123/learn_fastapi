import bcrypt


class HashHelper:
    @staticmethod
    def hash_password(password: str) -> str:
        """哈希密码加密"""
        # bcrypt.gensalt() 生成盐，并将其用于密码加密
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')  # 返回字符串形式

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """校验密码"""
        # bcrypt.checkpw() 校验明文密码与哈希密码是否匹配
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


# if __name__ == '__main__':
#     # 生成哈希密码
#     hashed = HashHelper.hash_password("123456")
#     print(f"Hashed password: {hashed}")
#
#     # 校验密码
#     is_valid = HashHelper.verify_password("123456", hashed)
#     print(f"Password is valid: {is_valid}")
