from datetime import datetime, timedelta
import jwt
import os
import pytz

def generate(email):
    payload = {
        'email': email,
        'exp': datetime.now(pytz.utc) + timedelta(hours=1)
    }
    secret_key = os.getenv('SECRET_KEY')
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        current_time = datetime.now(pytz.utc)
        expiration_time = datetime.fromtimestamp(payload['exp'], pytz.utc)
        if current_time > expiration_time:
            return False
        return True
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return False
