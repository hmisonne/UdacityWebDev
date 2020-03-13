import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from cerberus import Validator

import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

v = Validator()

v.schema = {
'question': {'required': True,'type': 'string', 'minlength': 10},
'answer': {'required': True},
'category': {'required': True,'type': 'integer', 'min': 1, 'max': 6},
'difficulty': {'required': True,'type': 'integer', 'min': 1, 'max': 5}
}

def paginate_questions(request, selection):
  page = request.args.get('page',1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE 
  current_questions = [question.format() for question in selection]
  return current_questions[start:end]

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/api/*": {"origins": "*"}})


  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,PATCH')
    return response
  

  @app.route('/categories', methods=['GET'])
  def get_all_categories():
    categories = Category.query.all()
    formated_categories = {} 
    for cat in categories:
      formated_categories[cat.id] = cat.type
    return jsonify(
      {'success': True,
      'categories': formated_categories})


  @app.route('/questions', methods=['GET'])
  def retrieve_questions():
    questions = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, questions)
    
    if len(current_questions) == 0:
      abort(404)

    categories = Category.query.all()
    formated_categories = {} 
    for cat in categories:
      formated_categories[cat.id] = cat.type
    
    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions':len(questions),
      'current_category': None,
      'categories': formated_categories})


  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def remove_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()
      # selection = Question.query.order_by(Question.id).all()
      # current_questions = paginate_questions(request, questions)
      return jsonify({
        'success': True,
        'question_id_deleted': question_id
      })
    except:
      abort(422)

  
  @app.route('/questions', methods=['POST'])
  def create_questions():
    body = request.get_json()
    new_question = body.get('question',None)
    new_answer  = body.get('answer',None)
    new_category = body.get('category',None)
    new_difficulty  = body.get('difficulty',None)
    search_term = body.get('searchTerm',None)

    try:
      if search_term:
        selection = Question.query.filter(Question.question.ilike(f'%{search_term}%')).order_by(Question.id).all()
        current_questions = [question.format() for question in selection]
        current_category = [question.category for question in selection]
        return jsonify({
          'success': True,
          'questions': current_questions,
          })  
      
      question_check = Question.query.filter(Question.question.ilike(f'%{new_question}%')).one_or_none()
      
      # Abort if invalid fields in the question or duplicate
      if v.validate(body) == False or question_check != None:
        # abort(400) # This specific number will still will return a 422 error code
        abort(422)


      question = Question(question=new_question,
                          answer=new_answer,
                          category=new_category,
                          difficulty=new_difficulty)

      question.insert()


      return jsonify({
        'success': True,
        'created': question.id,
        })

    except:
      abort(422)

  @app.route('/categories/<category_id>/questions', methods=['GET'])
  def search_questions_by_category(category_id):

    try:
      selection = Question.query.filter(Question.category == category_id).order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)
      current_category = Category.query.get(category_id).type

      return jsonify({
        'success': True,
        'questions': current_questions,
        'current_category':current_category,
        'total_questions':len(selection)
        })    

    except:
      abort(404)


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_quizz_questions():
    body = request.get_json()
    previous_questions = body.get('previous_questions',[])
    quiz_category = body.get('quiz_category',None)

    try:
      if quiz_category['id'] == 0:
        selection = Question.query.all()
      else:
        selection = Question.query.filter(Question.category == quiz_category['id']).all()

      random_selection = random.sample(selection, len(selection))
      for question in random_selection:
        if question.format()['id'] not in previous_questions:
          current_question = question.format()
          break
      return jsonify({
        'success': True,
        'question': current_question
        })
    except:
      abort(422)


  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Request unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad request"
      }), 400

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Internal Server Error"
      }), 500

  return app

    