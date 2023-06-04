import sys
sys.path.append("..")
from database import create_connection
from jwt_token import generate

class EmailNotFound(Exception):
    pass
class EmailAlreadyExists(Exception):
    pass
class WrongPassword(Exception):
    pass


def getByEmail(user_email):
    try:
        db = create_connection()
        query = 'SELECT * FROM users WHERE email = %s;'
        db["cursor"].execute(query, (user_email,))
        user = db["cursor"].fetchone()
        if user:
            return user
        return None
    except Exception as e:
        print(e)
        raise e
    finally:
        db["cursor"].close()
        db["conn"].close()

def register(username, password, email):
    try:
        user = getByEmail(email)
        if user:
            raise EmailAlreadyExists('there is already a user with this email')
        db = create_connection()
        query = 'INSERT INTO users (username, password, email) VALUES (%s, %s, %s)'
        db["cursor"].execute(query, (username, password, email))
        db["conn"].commit()
        token = generate(email)
        return token
    except Exception as e:
        raise e
    finally:
        db["cursor"].close()
        db["conn"].close()

def login(email, password):
    try:
        user = getByEmail(email)
        if not user:
            raise EmailNotFound('Could not find user with that email')
        if user[2] == password:
            token = generate(email)
            return token
        else:
            raise WrongPassword('Wrong password')
    except Exception as e:
        print(e)
        raise e