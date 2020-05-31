from app.api import bp
from app.models import Task
from flask import jsonify, request
from app.models import Task
from app import db

@bp.route('/tasks/<int:userId>', methods=['GET'])
def get_tasks(userId):
    print(userId)
    tasks = Task.query.filter_by(user_id = userId).all()
    tasks_dict = [task.to_dict() for task in tasks]
    return jsonify(tasks_dict)

@bp.route('/tasks/delete', methods=['POST'])
def delete_task():
    task_to_del = Task.query.filter_by(user_id = request.get_json()['user_id'],
                                       id = request.get_json()['task_id']).one()
    db.session.delete(task_to_del)
    db.session.commit()
    response = jsonify(task_to_del.to_dict())
    response.status_code = 201
    return response