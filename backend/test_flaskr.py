import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.db_host = os.getenv('DB_HOST', 'localhost:5432')  
        self.database_name = os.getenv('DB_NAME', 'trivia_test')  
        self.database_path = 'postgresql://{}/{}'.format(self.db_host, self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        self.assertTrue(len(data["categories"]) > 0)
    
    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(len(data["questions"]) > 0)

    def test_create_question(self):
        new_question = {
            'question': 'What is the avg. familiy income in Fremont',
            'answer': '20 k',
            'difficulty': 1,
            'category': 5
        }
        total_questions_old = len(Question.query.all())
        res = self.client().post("/questions", json=new_question)
        data = json.loads(res.data)
        total_questions_new = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(total_questions_new - total_questions_old, 1)

    def test_delete_question(self):
        total_questions = len(Question.query.all())
        res = self.client().delete("/questions/1")
        data = json.loads(res.data)
        total_questions_after_delete = len(Question.query.all())
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(total_questions - total_questions_after_delete, 1)

    def test_delete_question_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message", "unprocessable"],)

    
    def test_get_question_search_with_results(self):
        res = self.client().post("/questions/search", json={"search": "Butter"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertEqual(len(data["questions"]), 1) 

    def test_search_question_does_not_exist(self):
        res = self.client().post("/questions/search", json={"search": "RuiRui"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_questions"], 0)
        self.assertEqual(len(data["questions"]), 0) 

    def test_get_questions_within_category(self):
        res = self.client().get("/category/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertEqual(len(data["questions"]), 5) 

    def test_quiz(self):
        new_quiz = {
            'category':1,
            'pre_question':[]
        }

        res = self.client().post("/quiz", json = new_quiz)
        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["question"]) > 0)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()