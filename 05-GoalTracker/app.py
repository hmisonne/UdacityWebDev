import os
from flask import Flask, request, abort, jsonify
from models import setup_db, Objective, Athlete, Coach
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from auth.auth import AuthError, requires_auth
from sqlalchemy.exc import SQLAlchemyError
import datetime


def create_app(test_config=None):
    # App initialization
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def index():
        return jsonify({
                'success' : True
                })

    @app.route('/objectives', methods=['GET'])
    @requires_auth('get:objectives')
    def get_objectives(token):
        # Visualize all objectives
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
    @requires_auth('post:objectives')
    def add_objective(token):
        # Add new objective and reformat the input date
        body = request.get_json()
        description = body.get('description',None)
        start_date = body.get('start_date',None).strip("'").split(",")
        end_date = body.get('end_date',None).strip("'").split(",")
        athlete_id = body.get('athlete_id',None)

        try:
            new_objective = Objective(
                description=description,
                start_date=datetime.datetime(int(start_date[0]), int(start_date[1]), int(start_date[2])),
                end_date=datetime.datetime(int(end_date[0]), int(end_date[1]), int(end_date[2])),
                athlete_id=athlete_id)
            new_objective.insert()

            return jsonify({
                'success': True,
                'objective': new_objective.format()
                })
        except:
            abort(422)

    @app.route('/athletes', methods=['GET'])
    def get_athlete():
        # Query all athletes
        try:
            athletes = Athlete.query.all()
            selection = [athlete.format() for athlete in athletes]
            return jsonify({
                'success': True,
                'athletes': selection
                })
        except:
            abort(422)

    @app.route('/athletes', methods=['POST'])
    def add_athlete():
        # Add new athlete
        body = request.get_json()
        name = body.get('name',None)
        goal = body.get('goal',None)
        weight = body.get('weight',None)
        height = body.get('height',None)
        age = body.get('age',None)

        try:
            new_athlete = Athlete(
                name = name,
                goal = goal,
                weight = weight,
                height = height,
                age = age,
               )
            new_athlete.insert()

            return jsonify({
                'success': True,
                'athlete': new_athlete.format()
                })
        except:
            abort(422)

    @app.route('/coaches', methods=['GET'])
    def get_coaches():
        # Query all coaches
        try:
            coaches = Coach.query.all()
            selection = [coach.format() for coach in coaches]
            return jsonify({
                'success': True,
                'coaches': selection
                })
        except:
            abort(422)

    @app.route('/coaches', methods=['POST'])
    def add_coach():
        # Add new coach
        body = request.get_json()
        name = body.get('name',None)
        specialty = body.get('specialty',None)
        try:
            new_coach = Coach(
                name=name,
                specialty=specialty
               )
            new_coach.insert()

            return jsonify({
                'success': True,
                'coach': new_coach.format()
                })
        except:
            abort(422)

    @app.route('/athletes/<athlete_id>', methods=['DELETE'])
    @requires_auth('delete:athlete')
    def remove_athlete(token, athlete_id):
        athlete = Athlete.query.filter(Athlete.id == athlete_id).one_or_none()
        if athlete == None:
            abort(404)
        try:
            athlete.delete()
            return jsonify({
                'success': True,
                'athlete_deleted': athlete_id
                })
        except:
            abort(422)

    @app.route('/athletes/<athlete_id>/objectives', methods=['GET'])
    @requires_auth('get:objectivesperathlete')
    def get_athlete_objectives(token, athlete_id):
        # Visualize the objectives assigned to one athlete
        athlete = Athlete.query.filter(Athlete.id == athlete_id).one_or_none()
        if athlete == None:
            abort(404)
        try:
            selection = athlete.objectives
            objectives = [objective.format() for objective in selection]
            return jsonify({
                'success': True,
                'athlete_id': athlete_id,
                'objectives': objectives,
                })
        except:
            abort(422)

    @app.route('/objectives/<objective_id>', methods=['PATCH'])
    @requires_auth('patch:objectives')
    def update_objective(token, objective_id):
        # Change a value of an objective
        selected_objective = Objective.query.filter(Objective.id == objective_id).one_or_none()
        if selected_objective == None:
            abort(404)

        body = request.get_json()
        new_description = body.get('description',None)
        new_start_date = body.get('start_date',None)
        new_end_date = body.get('end_date',None)
        new_athlete_id = body.get('athlete_id',None)

        try:
            if new_description != None:
                selected_objective.description = new_description
            if new_start_date != None:
                selected_objective.start_date = new_start_date
            if new_end_date != None:
                selected_objective.end_date = new_end_date
            if new_athlete_id != None:
                selected_objective.athlete_id = new_athlete_id

            selected_objective.update()



            return jsonify({
                'success': True,
                'objective': selected_objective.format()
                })
        except:
            abort(422)

    @app.route('/objectives/<objective_id>', methods=['DELETE'])
    @requires_auth('delete:objectives')
    # Remove an objective from the database
    def remove_objective(token, objective_id):
        objective = Objective.query.filter(Objective.id == objective_id).one_or_none()
        if objective == None:
            abort(404)
        try:
            objective.delete()
            return jsonify({
                'success': True,
                'objective_deleted': objective_id
                })
        except:
            abort(422)

    @app.errorhandler(422)
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

    @app.errorhandler(405)
    def notallowed(error):
        return jsonify({
                        "success": False, 
                        "error": 405,
                        "message": "method not allowed"
                        }), 405

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

    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify({
          "success": False,
          "error": e.status_code,
          "message": e.error['description']
          }), e.status_code

    return app

app = create_app()


if __name__ == '__main__':
    app.run(debug=True)