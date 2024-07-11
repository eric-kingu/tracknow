from flask import Blueprint, request, jsonify, url_for
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models import db, User, Laptime

from functools import wraps
from decouple import config

routes = Blueprint('routes', __name__)

# api key authentication
api_key = config("API_KEY")

def require_api_key(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        provided_api_key = request.headers.get('x-api-key')
        if not provided_api_key or provided_api_key != api_key:
            return jsonify({'message': 'Invalid API key'}), 401
        return view_function(*args, **kwargs)
    return decorated_function


# Hello :)
@routes.route('/api/v1/hello', methods=['GET'])
def index():
    return jsonify({"msg": 'Track Now...'})

# Create a new user with username and password.
@routes.route('/api/v1/users', methods=['POST'])
@require_api_key
def new_user():
    new_user = request.get_json()
    # { "username" : "your_username",
    #"password" :  "your_password"}  
    if new_user['username'] is None or new_user['password'] is None:
        return jsonify({"msg": "Missing required fields"}), 400

    if User.query.filter_by(username=new_user['username']).first() is not None:
        return jsonify({"msg": "User Exists"}), 400

    user = User(username=new_user['username'])
    user.hash_password(new_user['password'])

    db.session.add(user)
    db.session.commit()

    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('routes.get_user', id=user.id, _external=True)})

# user changes/uploads profile_picture
@routes.route('/api/v1/users/<int:user_id>/profile_picture', methods=['PUT'])
@require_api_key
@jwt_required()
def update_user_profile_picture(user_id):
    current_user_id = get_jwt_identity()

    # Ensure the user is updating their own information
    if current_user_id != user_id:
        return jsonify({'msg': 'Permission denied'}), 403

    data = request.get_json()
    profile_picture_url = data.get('profile_picture_url', None)

    if profile_picture_url is None:
        return jsonify({'msg': 'No profile picture URL provided'}), 400

    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'User not found'}), 404

    user.update_profile_picture(profile_picture_url)

    return jsonify({'msg': 'Profile picture updated successfully', 'user': user.to_dict()}), 200

# update route for nationality,username,password change.
@routes.route('/api/v1/users/<int:user_id>/update', methods=['PUT'])
@require_api_key
@jwt_required()
def update_user_info(user_id):
    current_user_id = get_jwt_identity()

    # Ensure the user is updating their own information
    if current_user_id != user_id:
        return jsonify({'msg': 'Permission denied'}), 403

    data = request.get_json()
    new_username = data.get('username', None)
    new_password = data.get('password', None)
    new_nationality = data.get('nationality', None)

    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'User not found'}), 404

    if new_username is not None and not user.update_username(new_username):
        return jsonify({'msg': 'Username already exists'}), 400

    if new_password is not None:
        user.update_password(new_password)

    if new_nationality is not None:
        user.update_nationality(new_nationality)

    return jsonify({'msg': 'User information updated successfully', 'user': user.to_dict()}), 200

# Login to tracknow with username and password.
@routes.route('/api/v1/login', methods=['POST'])
@require_api_key
def login_user():
    login_user = request.get_json()
    user = User.query.filter_by(username=login_user['username']).first()
    if user and user.verify_password(login_user['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'msg': 'Login Success', 'token': access_token})
    else:
        return jsonify({'msg': 'Login Failed'}), 401

# Route to check someone on the database.   
@routes.route('/api/v1/users/<int:id>', methods=['GET'])
@require_api_key
@jwt_required()
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'msg': "User does not exist."})
    return jsonify({'username': user.username})

# Route to list all users
@routes.route('/api/v1/users', methods=['GET'])
@require_api_key
def get_users():
    users = User.query.filter_by().all()
    return jsonify([u.to_dict() for u in users]), 200

# Route to check if we are logged in with our unique jwt token.
@routes.route('/api/v1/protected', methods=['GET'])
@require_api_key
# Include bearer token from login_user() to  verify we are logged in and are in session.
@jwt_required()
def get_identity():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    # Check if user exists
    if user:
        return jsonify({'message': 'User found', 'name': user.username})
    else:
        return jsonify({'message': 'User not found'}), 404

# Logged in user adds laptime.
@routes.route('/api/v1/user/laptimes', methods=['POST'])
@require_api_key
@jwt_required()
def add_laptime():
    user_id = get_jwt_identity()
    loggedin_user = User.query.filter_by(id=user_id).first()
    
    laptime_data = request.get_json()

    car = laptime_data['car']
    track = laptime_data['track']
    time = laptime_data['time']
    simracing = laptime_data['simracing']
    platform = laptime_data['platform']
    youtube_link = laptime_data['youtube_link']
    comment = laptime_data['comment']

    if not car or not track or not time:
        return jsonify({'msg': 'Missing required fields'}), 400

    laptime = Laptime(
        user_id=user_id,
        car=car,
        track=track,
        time=time,
        simracing=simracing,
        platform=platform,
        youtube_link=youtube_link,
        comment=comment
    )

    db.session.add(laptime)
    db.session.commit()

    return jsonify({"Laptime Added Successfully": laptime.to_dict(), "by": loggedin_user.username}), 201

# Logged in user gets all the laptimes they posted on tracknow.
@routes.route('/api/v1/user/laptimes', methods=['GET'])
@require_api_key
@jwt_required()
def get_user_laptimes():
    user_id = get_jwt_identity()
    laptimes = Laptime.query.filter_by(user_id=user_id).all()
    
    return jsonify([lt.to_dict() for lt in laptimes]), 200

# Logged in user gets one laptime they selected.
@routes.route('/api/v1/user/laptimes/<int:id>', methods=['GET'])
@require_api_key
@jwt_required()
def get_user_laptime(id):
    user_id = get_jwt_identity()
    laptime = Laptime.query.filter_by(id=id, user_id=user_id).first()
    return jsonify(laptime.to_dict()), 200

# Global - get all laptimes posted around the world.
@routes.route('/api/v1/laptimes', methods=['GET'])
@require_api_key
def get_laptimes():
    # TODO introduce randomness, recently added 
    laptimes = Laptime.query.all() #Laptime.query.filter_by().all()

    return jsonify([lt.to_dict() for lt in laptimes]), 200

# Global - get one user laptime selected.
@routes.route('/api/v1/users/<int:user_id>/laptimes/<int:laptime_id>', methods=['GET'])
@require_api_key
@jwt_required()
def get_laptime(user_id, laptime_id):
    laptime = Laptime.query.filter_by(id=laptime_id, user_id=user_id).first()

    if laptime is None:
        return jsonify({'msg': 'Laptime not found'}), 404

    laptime_data = laptime.to_dict()
    user = User.query.filter_by(id=user_id).first()
    laptime_data['user'] = user.to_dict()

    return jsonify(laptime_data), 200