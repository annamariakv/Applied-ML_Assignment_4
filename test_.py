#!/usr/bin/env python
# coding: utf-8

# In[5]:


import unittest
import joblib
from score import score
import subprocess
import time
import json
from app import app
import os
import requests

class TestScore(unittest.TestCase):
    def setUp(self):
        self.model = joblib.load("D:\\Cmi\\Applied ML\\assignment_3\\trained_model.joblib")

    def test_score_function(self):
        prediction, propensity = score("This is a text.", self.model, 0.5)
        self.assertIsNotNone(prediction)
        self.assertIsNotNone(propensity)
        self.assertIsInstance(prediction, int)
        self.assertIsInstance(propensity, float)
        self.assertIn(prediction, [0, 1])
        self.assertTrue(0.0 <= propensity <= 1.0)

        # Additional functional tests can be added here.

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.proc = subprocess.Popen(['flask', 'run', '--port=5000'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)  # Give Flask a moment to start

    def tearDown(self):
        if self.proc:
            self.proc.terminate()
            self.proc.wait()

    def test_flask_app_response(self):
        response = self.app.post('/score', json={'text': 'This is a test text.'})
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIsInstance(data['prediction'], int)
        self.assertIsInstance(data['propensity'], float)
        self.assertTrue(0.0 <= data['propensity'] <= 1.0)

class TestDocker(unittest.TestCase):
    def setUp(self):
        subprocess.run(["docker", "build", "-t", "my-flask-app", "."])
        self.container_id = subprocess.check_output(["docker", "run", "-d", "-p", "5000:5000", "my-flask-app"]).decode('utf-8').strip()

    def tearDown(self):
        subprocess.run(["docker", "stop", self.container_id])
        subprocess.run(["docker", "rm", self.container_id])

    def test_docker_app_response(self):
        time.sleep(5)  # Wait for the container to start properly
        response = requests.get("http://localhost:5000/score")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"output": "sample output"})

if __name__ == '__main__':
    # Run the unit tests
    unittest.main()


# In[ ]:




