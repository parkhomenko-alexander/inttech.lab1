import os
import json
import sys
from models import User, Task
from app import app, db, jwt
from flask import request, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, logout_user
from flask_jwt_extended import jwt_required, current_user, set_access_cookies, get_csrf_token


@app.route('/', methods=['GET'])
def index():
    return('da')


@app.route('/user', methods=['POST'])
def user():
    params = request.form

    if ('login' not in params or 'pas' not in params):
        return {
            "msg": 'add attributes'
        }, 400

    user = User.authenticate(**params)

    if (user == 0):
        user = User(**params)
        access_token = user.get_token()
        response = jsonify({"msg": user.save_to_db(),
                            "access_token": access_token})
        set_access_cookies(response, access_token)
        return response, 201
    elif (user == 1):
        return {
            "msg": 'wrong password',
        }, 400
    else:
        access_token = user.get_token()
        response = jsonify({'access_token': access_token})
        set_access_cookies(response, access_token)
        return response, 201


@app.route('/todo', methods=['POST'])
@jwt_required()
def todo():
    params = request.form
    user_id = current_user.id
    task = Task(**params)
    task.user_id = user_id
    task.save_to_db()
    return 'task added with number ' + str(task.id), 201


@app.route('/todo/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_todo(id):
    task = Task.query.filter(Task.id == id).first()
    if (task is None):
        return 'task with number ' + str(id) + ' is not exists', 418
    else:
        task.delete_from_db()
        return 'task with number ' + str(id) + ' is deleted', 202


@app.route('/todo/<int:id>', methods=['PUT'])
@jwt_required()
def change_todo(id):
    task = Task.query.filter(Task.id == id).first()
    if (task is None):
        return 'task with number ' + str(id) + ' is not exists', 418
    else:
        task.description = request.form['description']
        task.save_to_db()
    return 'task with number ' + str(id) + ' is changed', 202


@app.route('/todo', methods=['GET'])
@jwt_required()
def get_todo():
    tasks = current_user.tasks
    response = {'login': current_user.login}
    for task in tasks:
        str_to_update = {f'id: {task.id}': f'description: {task.description}'}
        response.update(str_to_update)
    # response = dict(reversed(list(response.items())))
    print(response, file=sys.stderr)
    return response, 200


@ jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(login=identity).one_or_none()
