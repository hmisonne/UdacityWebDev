import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Coach, Athlete, Objective, Coach

coach_token = os.environ.get('COACH_TOKEN')
athlete_token = os.environ.get('ATHLETE_TOKEN')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASS')

class GoalTrackerTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "goaltracker_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(db_user, db_password,'localhost:5432', self.database_name)
        self.headers_coach = {'Content-Type': 'application/json', 'Authorization': coach_token}
        self.headers_athlete = {'Content-Type': 'application/json', 'Authorization': athlete_token}
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_objective = {
            "description": "Go to the gym twice a week for 30 min",
            "athlete_id": 3,
            "start_date":"2020,1,1",
            "end_date":"2020,12,12"
        }

        self.new_athlete = {
            "name": "Vanessa",
            "goal": "Loose 5 kg",
            "weight": 40,
            "height": 170,
            "age": 30
        }

        self.new_coach = {
            "name": "Henry",
            "specialty": "Woman Fitness"
        }
        
        
        
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_index(self):
        res = self.client().get('/')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_objectives(self):
        res = self.client().get('/objectives', headers=self.headers_athlete)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['objectives'], list)

    def test_401_invalid_header_add_objectives(self):
        res = self.client().post('/objectives', json=self.new_objective)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], "Authorization header is expected.")
        self.assertEqual(data['success'], False)
    
    def test_add_objectives(self):
        res = self.client().post('/objectives', headers=self.headers_coach, json=self.new_objective)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['objective'])

    def test_get_all_athletes(self):
        res = self.client().get('/athletes')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['athletes'], list)
    
    def test_create_athlete(self):
        res = self.client().post('/athletes', json=self.new_athlete)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['athlete'])

    def test_create_coach(self):
        coach = Coach.query.all()
        res = self.client().post('/coaches', json=self.new_coach)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['coach'])

    def test_get_all_coaches(self):
        res = self.client().get('/coaches')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['coaches'], list)


    def test_delete_athlete(self):
        res = self.client().delete('/athletes/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], "Authorization header is expected.")
        self.assertEqual(data['success'], False)

    def test_404_athlete_not_found_get_objectives_per_athlete(self):
        res = self.client().get('/athletes/200/objectives', headers=self.headers_athlete)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data['success'], False)

    def test_edit_objectives(self):
        res = self.client().patch('/objectives/1', headers=self.headers_coach, json={'description':'Test'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['objective'])
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()