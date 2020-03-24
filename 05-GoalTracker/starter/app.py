import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import User, Objective

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

  return app

APP = create_app()

@app.route('/objectives', methods=['GET'])
def get_all_objectives():
	try:
		selection = Objective.query.all()
		objectives = [objective.format() for objective in selection]
		return jsonify({
			'success' : True,
			'objectives': objectives
			})
	except:
		abort(422)

@app.route('/objectives', methods=['POST'])
def add_objective():
	body = request.get_json()
	name = body.get('name',None)
	start_date = body.get('start_date',None)
	end_date = body.get('end_date',None)
	frequency = body.get('frequency',None)
	user_id = body.get('user_id',None)
	try:
		new_objective = Objective(
			name=name,
			start_date=start_date,
			end_date=end_date, 
			frequency=frequency,
			user_id=user_id)
		new_objective.insert()

		return jsonify({
			'success': True,
			'objective': objective.format()
			})
	except:
		abort(422)
@app.route('/users/<user_id>/objectives', methods=['GET'])
def get_user_objectives():
	try:
		user = User.query.get(user_id)
		selection = user.objectives
		objectives = [objective.format() for objective in selection]
		return jsonify({
			'success': True,
			'user_id': user_id
			'objectives': objectives,
			})
	except:
		abort(422)

@app.route('/objectives/<objective_id>', methods=['PATCH'])
def update_objective(objective_id):
	selected_objective = Objective.query.filter(Objective.id == objective_id).one_or_none()

	if selected_objective == None:
		abort(404)

	body = request.get_json()
	name = body.get('name',None)
	start_date = body.get('start_date',None)
	end_date = body.get('end_date',None)
	frequency = body.get('frequency',None)
	user_id = body.get('user_id',None)

	try:
		selected_objective['name'] = name
		selected_objective['start_date'] = start_date
		selected_objective['end_date'] = end_date
		selected_objective['frequency'] = frequency

		selected_objective.update()

		return jsonify({
			'success': True,
			'objective': selected_objective
			})
	except:
		abort(422)

@app.route('/objectives/<objective_id>', methods=['DELETE'])
def remove_objective(objective_id):
	objective = Objective.query.filter(Objective.id = objective_id).one_or_none()
	if objective == None:
		abort(404)
	try:
		objective.delete()
		return jsonify({
			'success': True,
			'objective_deleted': objective.format()
			})
	except:
		abort(422)

@app.errorhandler(422):
def unprocessable(error):
	return jsonify({
		"success": False,
		"error":422,
		"message": "unprocessable"
		}),422

@app.errorhandler(404)
def notfound(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Internal Server Error"
      }), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad request"
      }), 400

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)