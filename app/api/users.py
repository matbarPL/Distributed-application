from flask import jsonify, request
from datetime import datetime
from flask_jwt_extended import (create_access_token)
from app.models import User

from app import bcrypt
from app import db
from app.api import bp

@bp.route('/users/register', methods=['POST'])
def register():
    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    email = request.get_json()['email']
    password_hash = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    created = datetime.utcnow()
    user = User(first_name=first_name, last_name=last_name, email=email,
                password_hash=password_hash, created = created)
    db.session.add(user)
    db.session.commit()
    result = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password_hash': password_hash,
        'created': created
    }
    response = jsonify({'result': result})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@bp.route('/users/login', methods=['POST'])
def login():
    email = request.get_json()['email']
    password = request.get_json()['password']
    result = ""
    user = User.query.filter_by(email=email).first()
    if user is None:
        result = jsonify({"error": "Invalid email"})
    else:
        user_password_hash = user.password_hash
        if bcrypt.check_password_hash(user_password_hash, password):
            access_token = create_access_token(
                identity={'first_name': user.first_name, 'last_name': user.last_name,\
                          'email': user.email})
            result = access_token
            print(result )
        else:
            print('else')
            result = jsonify({"error": "Invalid password"})

    print(user)
    return result

