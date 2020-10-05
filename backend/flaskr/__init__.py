import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import func, or_, and_, not_

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 1

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resource={r"*/api/*": {'origins': '*'}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type, Authorization')
    response.headers.add(
        'Access-Control-Allow-Methods',
        'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():

    categories = Category.query.all()

    return jsonify({
        'success': True,
        'categories': [category.format() for category in categories],
    }), 200

  # create new category
  @app.route('/categories', methods=['POST'])
  def new_category():

    category_type = request.get_json()['type']

    category = Category(type=category_type)

    category.insert()

    return jsonify(
        {
            'success': True,
        }), 200

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
  def get_questions():
    # page
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 10
    end = start + 10
    # questions
    questions = Question.query.all()
    formated_questions = [question.format() for question in questions]

    # categories
    categories = Category.query.all()

    return jsonify({
        'success': True,
        'questions': formated_questions[start:end],
        'total_questions': len(formated_questions),
        'categories': [category.format() for category in categories],
        'current_category': 0
    }), 200

  '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):

    question = Question.query.get(question_id)

    if question is not None:
      question.delete()

    return jsonify({
        'deleted': question_id,
        'success': True
    }), 200

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
  def new_question():

    question = Question(
        question=request.get_json()['question'],
        answer=request.get_json()['answer'],
        category=request.get_json()['category'],
        difficulty=request.get_json()['difficulty']
    )

    question.insert()

    return jsonify({
        'success': True,
    }), 200

  '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():

    search_term = request.get_json()['searchTerm']

    questions = Question.query.filter(
        Question.question.ilike('%' + search_term + '%')
    ).all()

    formated_questions = [question.format() for question in questions]

    return jsonify({
        'success': True,
        'questions': formated_questions,
        'total_questions': len(formated_questions),
        'current_category': 0
    }), 200

  '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):

    questions = Question.query.filter_by(category=str(category_id)).all()

    formated_questions = [question.format() for question in questions]

    return jsonify({
        'questions': formated_questions,
        'total_questions': len(formated_questions),
        'current_category': category_id,
        'success': True
    }), 200

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
  def quizzes():

    quiz_category = request.get_json(force=True)['quiz_category']
    previous_questions = request.get_json(force=True)['previous_questions']

    category_id = int(quiz_category['id'])

    question = {}
    formated_question = None

    if category_id == 0:
        question = Question.query.filter(
            not_(
                Question.id.in_(previous_questions))).order_by(
            func.random()).first()

    else:
        question = Question.query.filter(
            Question.category == str(category_id)).filter(
            not_(
                Question.id.in_(previous_questions))).order_by(
            func.random()).first()

    if question:
        formated_question = question.format()

    return jsonify({
        'question': formated_question,
        'success': True,
    }), 200

  '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
  @app.errorhandler(400)
  def not_found(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request',
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource not found',
    }), 404

  @app.errorhandler(405)
  def not_found(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'Method not allowed',
    }), 405

  @app.errorhandler(422)
  def not_found(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable',
    }), 422

  @app.errorhandler(500)
  def not_found(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal server error',
    }), 500

  return app