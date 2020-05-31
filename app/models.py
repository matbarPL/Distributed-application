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
    token = db.Column(db.String(240))
    admin = db.Column(db.Boolean, default= False)

    def set_token(self):
        self.token = create_access_token(identity=
                                         {'id':self.id,
                                          'first_name': self.first_name,
                                          'last_name': self.last_name,
                                          'email': self.email,
                                          'admin': self.admin})

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {'id': self.id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email,
                'admin': self.admin}

    def __repr__(self):
        return '<User first name {} User last name {} Password {} Token{}>'.format(self.first_name, self.last_name,self.password_hash,self.token)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    init_number = db.Column(db.Integer)
    number_of_classrooms = db.Column(db.Integer)
    number_of_slaves = db.Column(db.Integer)
    max_iteration_number = db.Column(db.Integer)
    mutation_probability = db.Column(db.Integer)
    cross_probability = db.Column(db.Integer)
    creation_time = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)

    def get_user_by_token(self, token):
        return User.query.filter_by(id = token).one()

    def to_dict(self):
        return {'id': self.id,
                'init_number': self.init_number,
                'number_of_classrooms': self.number_of_classrooms ,
                'number_of_slaves': self.number_of_slaves ,
                'max_iteration_number': self.max_iteration_number,
                'mutation_probability':self.mutation_probability,
                'cross_probability':self.cross_probability,
                'creation_time':self.creation_time,
                'user_id':self.user_id}
