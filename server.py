from flask import Flask, request
from dotenv import load_dotenv
from repositories.User import login, register, getByEmail
from jwt_token import verify_token, return_email
from spotify import get_access_token, get_list_of_songs
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return {'error': 'preperties missing'},400
    try:
        token = login(email, password)
    except Exception as e:
        return {'error': str(e)},401
    else:
        return {'token': token},200

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    if not email or not password or not username:
        return {'error': 'preperties missing'},400
    try:
        token = register(username, password, email)
    except Exception as e:
        return {'error': str(e)},401
    else:
        return {'token': token},201
    
@app.route('/token', methods=['GET'])
def check_token():
    token = request.headers.get('Authorization')
    print(token)
    checked = verify_token(token)
    if checked:
        return {'message': 'Token is valid'}, 200
    else:
        return {'error': 'Unauthorized'}, 401
    
@app.route('/spotify', methods=['GET'])
def check_spotify():
    try:
        token = get_access_token()
    except Exception as e:
        return {'error': str(e)},401
    else:
        print('foi')
        return token,200
    
@app.route('/search/<song>')
def search_for_songs(song):
    try:
        list_of_songs = get_list_of_songs(song)
    except Exception as e:
        return {'error': str(e)},401
    else:
        print('foi')
        return list_of_songs,200
    
@app.route('/user')
def get_user():
    token = request.headers.get('Authorization')
    print('A')
    email = return_email(token)
    print(email)
    if email:
        try:
            user = getByEmail(email)
            print(user)
            if user:
                user_object = {
                    'user_id': user[0],
                    'username': user[1],
                    'user_email': user[3]
                }
                return user_object,200
            return {'error': 'Invalid email'}
        except Exception as e:
            return {'error': str(e)},401
    else:
        return {'error': 'Invalid token'},401