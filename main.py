import json
from flask_cors import CORS
from flask import Flask, request, render_template
from sqlalchemy.exc import IntegrityError

from models import db, Logs

''' Begin boilerplate code '''
def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SECRET_KEY'] = "MYSECRET"
  CORS(app)
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()

''' End Boilerplate Code '''

@app.route('/')
def index():
  return 'Hello World!'

@app.route('/app')
def client_app():
  return app.send_static_file('app.html')

@app.route('/logs', methods=['POST'])
def create_log():
    data = request.get_json()
    log = Logs(stream=data['stream'], studentId=data['studentId'])
    db.session.add(log)
    db.session.commit()
    return 'Log created!', 201

@app.route('/logs', methods=['GET'])
def get_logs():
    logs = Logs.query.all()
    logs = [log.toDict() for log in logs]
    return json.dumps(logs)

@app.route('/logs/<id>', methods=['PUT'])
def update_log(id):
    data = request.get_json()
    log = Logs.query.get(id)
    if not log:
        return 'Log does not exist!', 404 
    if 'stream' in data:
        log.stream = data['stream']
    db.session.add(log)
    db.session.commit()
    return 'Log Updated!', 201

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)