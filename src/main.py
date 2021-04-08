"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Todo

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/todos', methods=['GET'])
def get_todo():

    todo_alls = Todo.query.all()
    result = list(map(lambda x: x.serialize(), todo_alls))
    return jsonify(result), 200

@app.route('/todos', methods=['POST'])
def add_todo():

    body = request.get_json()
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'label' not in body:
        raise APIException('You need to specify the tasks', status_code=400)        

    newTodo = Todo(task=body['label'], is_done=body['done'])
    db.session.add(newTodo)
    db.session.commit()
    return "ok", 200

@app.route('/todos/<int:id>', methods=['DELETE'])
def remove_todo(id):

    item = Todo.query.get(id)
    if item is None:
        raise APIException('Task not found', status_code=404)

    db.session.delete(item)
    db.session.commit()
    return jsonify("Task deleted successfully."), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)