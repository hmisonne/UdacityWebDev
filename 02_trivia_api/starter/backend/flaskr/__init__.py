import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
  page = request.args.get('page',1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE 
  current_questions = [question.format() for question in selection]
  return current_questions[start:end]

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  # app = Flask(__name__, root_path='frontend/')
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,PATCH')
    return response
  
  
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_all_categories():
    categories = Category.query.all()
    formated_categories = [cat.format() for cat in categories]
    return jsonify({'categories': formated_categories})
    # return render_template('pages/search_venues.html', results=response, search_term=request.args.get('search_term_location', ''))

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 


  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_all_questions():
    questions = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, questions)
    return jsonify({'questions': current_questions,
                    'total_num_questions':len(questions),
                    'current_category':'',
                    'categories':''})
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def remove_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()
      if question is None:
        abort(404)

      question.delete()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, questions)
      return jsonify({
        'questions': current_questions,
        'total_num_questions':len(selection),
        'current_category':'',
        'categories':''})
    except:
      abort(422)



  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_questions():
    body = request.get_json()
    new_question = body.get('question',None)
    new_answer  = body.get('answer',None)
    new_category = body.get('category',None)
    new_difficulty  = body.get('difficulty',None)

    try:
      question = Question(question=new_question,
                          answer=new_answer,
                          category=new_category,
                          difficulty=new_difficulty)
      question.insert()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, questions)
      return jsonify({
        'success': True,
        'created': question.id,
        'questions': current_questions,
        'total_num_questions':len(selection)
        })

    except:
      abort(422)
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions_search', methods=['POST'])
  def search_question():
    body = request.get_json()
    search_term = body['search_term']
    try:
      selection = Question.query.filter(Question.question.ilike(f'%{search_term}%')).order_by(Question.id).all()
      current_questions = paginate_questions(request, questions)
      return jsonify({
        'success': True,
        'created': question.id,
        'questions': current_questions,
        'total_num_questions':len(selection)
        })    
    except:
      abort(422)


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/questions/<category>', methods=['GET'])
  def search_questions_by_category(category):
    try:
      selection = Question.query.filter(Question.category == category).order_by(Question.id).all()
      current_questions = paginate_questions(request, questions)
      return jsonify({
        'success': True,
        'created': question.id,
        'questions': current_questions,
        'total_num_questions':len(selection)
        })    
    except:
      abort(422)


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
  @app.route('/quizz', methods=['POST'])
  def get_quizz_questions():
    body = request.get_json()
    category = body.get('category',None)
    previous_question = body.get('previous_question',[])
    try:
      if category == None:
        selection = Question.query.filter(Question.category == category).all()
      else:
        selection = Question.query.filter(Question.category == category).all()
      
      random_selection = random.shuffle(selection)
      for question in random_selection:
        if question not in previous_question:
          current_question = question
      if current_question == None:
        return jsonify({
          'end_of_test': True
          })
          
      return jsonify({
        'success': True,
        'question': question.question
        'answer': question.answer
        'previous_question': previous_question.append(current_question)
        })
    except:
      abort(422)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Request unprocessable"
      }), 422
  return app

    