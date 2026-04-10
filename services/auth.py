from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from core.settings import settings


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(original_password: str):
    return bcrypt_context.hash(original_password)

def verify_password(original_password: str, hashed_password: str):
    return bcrypt_context.verify(original_password, hashed_password)

def create_access_token(username: str, room_id: int, password: str, expires_in: timedelta):
    encode = {'username': username, 'room_id': room_id, 'password': password, 'exp': datetime.now(timezone.utc) + expires_in}
    return jwt.encode(encode, settings.SECRET_KEY, algorithm="HS256")

def get_current_user(token: str):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    username = payload.get("username")
    room_id = payload.get("room_id")
    password = payload.get("password")
    
    if not username or not room_id or not password:
        raise ValueError("Not found")
    return {"username": username, "room_id": room_id, "password": password}