from flask import Flask, jsonify, request, send_from_directory
from datetime import datetime
from flask_jwt_extended import (create_access_token)
from app.models import User
from werkzeug.utils import secure_filename

from app import bcrypt
from app import db
from app.api import bp

import os
app = Flask(__name__)

UPLOAD_FOLDER = "/home/lukasz/nauka/AIIR/frontback/Distributed-application/app/api/dataFiles"
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
PROGRAM_FOLDER = "/home/lukasz/cloud/program"
PROGRAM_TIMETABLE_FILE = "/home/lukasz/cloud/program/timetable.xlsx"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROGRAM_FOLDER'] = PROGRAM_FOLDER
app.config['PROGRAM_TIMETABLE_FILE'] = PROGRAM_TIMETABLE_FILE

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
        else:
            result = jsonify({"error": "Invalid password"})

    return result


@bp.route('/uploadfile', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({"error": "File type not allowed"})
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return jsonify({"error": "No selected file"})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['PROGRAM_FOLDER'], filename))
            return "done"
        else:
            return jsonify({"error": "File type not allowed"})
    return jsonify({"error": "File type not allowed"})


@bp.route('/users/function', methods=['GET', 'POST'])
def generateTimetable():
    number_of_classrooms = request.get_json()['number_of_classrooms']
    number_of_slaves = request.get_json()['number_of_slaves']
    max_iteration_number = request.get_json()['max_iteration_number']
    mutation_probability = request.get_json()['mutation_probability']
    cross_probability = request.get_json()['cross_probability']

    mpiNodes = ''
    if number_of_slaves > 0:
    	mpiNodes = '-H master,'
    	for x in range(int(number_of_slaves)):
    		mpiNodes += 'uslave' + str(x + 1) + ','
    mpiNodes = mpiNodes[:-1] + ' '

    command = ('mpirun ' + mpiNodes + 'python CSP.py '
                                       + str(number_of_slaves) + ' '
                                       + str(max_iteration_number) + ' '
                                       + str(mutation_probability) + ' '
                                       + str(cross_probability) + ' '
                                       + str(number_of_classrooms))

    print command
    os.chdir(app.config["PROGRAM_FOLDER"])
    os.system(command)

    if(os.path.isfile(app.config["PROGRAM_TIMETABLE_FILE"])):
        return "done"
    return jsonify({"error": "error: Server problem"})


@bp.route('/download')  #/<path:filename>
def download():
    #filename = request.get_json()['filename']
    path = "timetable.xlsx"
    return send_from_directory(app.config["PROGRAM_FOLDER"], path, as_attachment=True, cache_timeout=30)

#@bp.route("/download/<path:path>")
#def get_file(path):
#    print "gowno"
#    return send_from_directory(UPLOAD_FOLDER, path, as_attachment=True)



@bp.route('/users/mpi', methods=['POST'])
def start_mpi():
    number_of_classrooms = request.get_json()['number_of_classrooms']
    command = 'mpirun python CSP.py {number_of_classrooms}'.format(number_of_classrooms=number_of_classrooms)
    number_of_slaves = request.get_json()['number_of_slaves']
    max_iteration_number = request.get_json()['max_iteration_number']
    mutation_probability = request.get_json()['mutation_probability']
    cross_probability = request.get_json()['cross_probability']

    print command
    os.chdir('/home/lukasz/nauka/AIIR/program')
    os.system(command)

    result = 'my_function()'
    return result
