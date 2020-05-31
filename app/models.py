from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from flask_jwt_extended import (create_access_token)
from flask import g
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(64))
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {'id': self.id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email}

    def __repr__(self):
        return '<User first name {} User last name {} Password {}>'.format(self.first_name, self.last_name,self.password_hash)