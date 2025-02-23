import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 10


def paginate_questions(request):
    page = request.args.get("page", 1, type=int)
    current_index = page - 1
    questions = Question.query.order_by(Question.id).limit(
        QUESTIONS_PER_PAGE).offset(current_index * QUESTIONS_PER_PAGE).all()
    return [question.format() for question in questions]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers",
                             "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods",
                             "GET,PUT,POST,DELETE,OPTIONS")
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests for all available categories.
    """

    @app.route("/categories")
    def get_categories():
        categories = Category.query.order_by(Category.type).all()

        if len(categories) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "categories": {category.id: category.type for category in categories}
            }
        )
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route("/questions")
    def get_questions():
        #questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request)
        categories = Category.query.order_by(Category.type).all()

        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "categories": {category.id: category.type for category in categories},
                "questions": current_questions,
                "total_questions": len(Question.query.all()),
            }
        )

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):

        question = Question.query.filter(
            Question.id == question_id).one_or_none()

        if question is None:
            abort(404)

        try:
            question.delete()
            current_questions = paginate_questions(request)

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                }
            )
        except Exception as ex:
            #print('delete question ', ex)
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_difficulty = body.get("difficulty", None)

        if new_question == None or new_answer == None or new_category == None or new_difficulty == None:
            abort(422)

        try:
            question = Question(question=new_question, answer=new_answer,
                                category=new_category, difficulty=new_difficulty)
            question.insert()

            current_questions = paginate_questions(request)

            return jsonify(
                {
                    "success": True,
                    "created": question.id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                }
            )
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        body = request.get_json()
        search = body.get("search", None)

        page = request.args.get("page", 1, type=int)
        current_index = page - 1
        current_questions = Question.query.order_by(Question.id).filter(
            Question.question.ilike(
                "%{}%".format(search)
            )).limit(QUESTIONS_PER_PAGE).offset(current_index * QUESTIONS_PER_PAGE).all()

        return jsonify(
            {
                "success": True,
                "questions": [current_question.format() for current_question in current_questions],
                "total_questions": len(Question.query.all()),
            }
        )

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/category/<int:category_id>/questions", methods=["GET", "POST"])
    def get_category_question(category_id):

        try:
            questions = Question.query.filter(Question.category == category_id)
        except Exception as ex:
            abort(422)

        if len(questions.all()) == 0:
            abort(404)

        try:
            return jsonify(
                {
                    "success": True,
                    "questions": [question.format() for question in questions],
                    "total_questions": len(Question.query.all()),
                }
            )
        except Exception as ex:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random question within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and show whether they were correct or not.
    """
    @app.route("/quiz", methods=["POST"])
    def play_quiz():
        body = request.get_json()
        category_id = body.get("category", None)
        pre_question = body.get("pre_question")

        category_questions = Question.query.filter(
            Question.category == category_id)
        if len(category_questions.all()) == 0:
            abort(404)
        try:
            questions = Question.query.order_by(Question.id).filter(
                Question.category == category_id).filter(Question.id.notin_((pre_question))).all()
            random_question = questions[random.randrange(
                0, len(questions))].format() if len(questions) > 0 else None

            if random_question is None:
                abort(422)

            return jsonify({
                'success': True,
                'question': random_question
            })
        except:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False,
                     "error": 404,
                    "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False,
                     "error": 422,
                    "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    return app
