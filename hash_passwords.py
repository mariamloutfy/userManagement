import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()  # Store as string

def check_password(hashed_password, plain_password):
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
