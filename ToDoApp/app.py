from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:noisette@localhost:5432/todoapp'
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)
  completed = db.Column(db.Boolean, default=False, nullable=False)
  list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

  def __repr__(self):
    return f'<Todo {self.id} {self.description}>'

class TodoList(db.Model):
  __tablename__ = 'todolists'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)
  completed = db.Column(db.Boolean, default=False, nullable=False)
  todos = db.relationship('Todo', backref = 'list', lazy = True, cascade="all, delete-orphan")

# db.create_all()

@app.route('/lists/<list_id>')
def get_list_of_todos(list_id):
	return render_template('index.html',
  lists=TodoList.query.order_by('id').all(),
  active_list=TodoList.query.get(list_id),
  todos=Todo.query.filter_by(list_id=list_id).order_by('id').all()
)

@app.route('/')
def index():
	return redirect(url_for('get_list_of_todos', list_id=1))

@app.route('/todos/create', methods=['POST'])
def create_todo():
	error = False
	body = {}
	try:
		description = request.get_json()['description']
		list_id = request.get_json()['list_id']
		todo = Todo(description=description, list_id=list_id)
		db.session.add(todo)
		db.session.commit()
		body['description'] = todo.description
	except:
		db.session.rollback()
		print(sys.exc_info())
		error = True
	finally:
		db.session.close()
	if error:
		abort (400)
	else:
		return jsonify(body)

@app.route ('/todoLists/create', methods=['POST'])
def create_todoList():
	error = False
	body = {}
	try:
		name = request.get_json()['name']
		todoList = TodoList(name=name)
		db.session.add(todoList)
		db.session.commit()
		body['name'] = todoList.name
		body['id'] = todoList.id

	except:
		db.session.rollback()
		print(sys.exc_info())
		error = True
	finally:
		db.session.close()
	if error:
		abort (400)
	else:
		return jsonify(body)


@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
	error = False
	try:
		completed = request.get_json()['completed']
		todo = Todo.query.get(todo_id)
		todo.completed = completed
		db.session.commit()
	except:
		db.session.rollback()
	finally:
		db.session.close()
	return redirect(url_for('index'))

@app.route('/lists/<list_id>/set-completed', methods=['POST'])
def set_completed_list(list_id):
	error = False
	body = {}
	try:
		completed = request.get_json()['completed']
		current_list = TodoList.query.get(list_id)
		current_list.completed = completed
		todos = current_list.todos
		# print(todos)
		# body['completed'] = completed
		# body['todos'] = []
		# for todo in todos:
		# 	body['todos'].append(todo.id)
		# 	todo.completed = completed
		db.session.commit()
	except:
		db.session.rollback()
	finally:
		db.session.close()
	return render_template('index')
	# return jsonify(body)

@app.route('/todos/<todo_id>/delete', methods=['DELETE'])
def delete_todo(todo_id):
	error = False
	try:
		Todo.query.filter_by(id=todo_id).delete()
		db.session.commit()

	except:
		db.session.rollback()
	finally:
		db.session.close()
	return jsonify({ 'success': True })

@app.route('/lists/<list_id>/delete', methods=['DELETE'])
def delete_list(list_id):
	error = False
	try:
		print(list_id,'deleted')
		TodoList.query.filter_by(id = list_id).delete()
		db.session.commit()
	except:
		print(list_id,'rollback')
		db.session.rollback()
	finally:
		db.session.close()
	return jsonify({ 'success': True })