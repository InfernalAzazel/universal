import bcrypt


def hash_password(password: str) -> str:
    """
    对用于存储的密码进行哈希处理。
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    根据用户提供的密码验证存储的密码
    """
    plain_password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    print(plain_password_bytes, hashed_password_bytes)
    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)
