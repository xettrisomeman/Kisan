import bcrypt
from sqlalchemy import select


def verify_password(plain_password, hashed_password):
    """Verify that the provided password matches the stored hashed password"""
    plain_password = str.encode(plain_password)
    hashed_password = str.encode(hashed_password)
    return bcrypt.checkpw(plain_password, hashed_password)


def get_password_hash(password):
    """Generate a hash for a password"""
    password = str.encode(password)
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt).decode()


def authenticate_user(db, schema, email: str, password: str):
    """Authenticate a user by email and password"""
    user = db.scalars(select(schema).filter(schema.email == email)).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
