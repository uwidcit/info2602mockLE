import json
from flask_cors import CORS
from flask import Flask, request, render_template, jsonify, url_for, redirect, send_from_directory
from sqlalchemy.exc import IntegrityError

from models import db, Log

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

'''SSR Version '''

@app.route('/', methods=['GET'])
def index():
  logs = Log.query.all()
  return render_template('index.html', logs=logs)

@app.route('/edit/<id>', methods=['GET'])
def edit_page(id):
  return render_template('edit.html', id=id)

@app.route('/edit/<id>', methods=['POST'])
def edit_action(id):
  data = request.form
  log = Log.query.get(id)
  if log:
    log.stream = data['stream']
    db.session.add(log)
    db.session.commit()
  return redirect(url_for('index'))

@app.route('/logs', methods=['POST'])
def create_log():
  data = request.form
  newlog = Log(stdid=data['stdid'], stream=data['stream'])
  db.session.add(newlog)
  db.session.commit()
  return redirect(url_for('index'))

# returns a count of how many times a particular stream appears in the table
@app.route('/stats', methods=['GET'])
def stats():
  logs = Log.query.all()
  stats = [0, 0, 0]
  for log in logs:
    stats[log.stream - 1] += 1
  return jsonify(stats)

''' END SSR Version '''


''' Begin CSR Version '''

@app.route('/app', methods=['GET'])
def home():
  return send_from_directory('static', 'index.html')

@app.route('/api/logs', methods=['GET'])
def get_log():
  logs = Log.query.all()
  logs = [ log.toDict() for log in logs]
  return jsonify(logs)

@app.route('/api/logs/<id>', methods=['PUT'])
def update_log(id):
  data = request.json
  log = Log.query.get(id)
  if log:
    log.stream = data['stream']
    db.session.add(log)
    db.session.commit()
  return jsonify({"message": f'Log with id {log.id} updated!'}), 201

@app.route('/api/logs', methods=['POST'])
def create_log2():
  data = request.json
  newlog = Log(stdid=data['stdid'], stream=int(data['stream']))
  db.session.add(newlog)
  db.session.commit()
  return jsonify({"message": f'Log created with id {newlog.id}'}), 201


''' END CSR Version '''

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)