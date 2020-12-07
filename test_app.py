import os
import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
from unittest.mock import patch

from app import create_app
from models import setup_db, Actor, Movie


EXECUTIVE_PRODUCER_CREDENTIALS='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii13c29yTGJuU3ZkVnZoc1BNeEdDMiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LXN2LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZmNkMDlhNWMwNThmODAwNmY0NTkzYjEiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjA3MzEyNDI3LCJleHAiOjE2MDczOTg4MjcsImF6cCI6IkxzN0tqT3pBd0pJTFBwVUplbE13MGhoZVRKSzE3bFlBIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.iAwej2zHUnrwlgO6362roc2xPwegQyg0_B4bvfleCTYvYui4KIqGoL_CJ9o4KohDBS--xuuP6d2lO2rBLmPzN3DV_5WpDqocri6uCOfZ3laFRwPpJc6kHPzcD0lOKQnorizXEmO9ndqBpgb5BmGzBB3pkmxUEbE0tyQFNv4X_wZv1-iT4MO71_MXbRPvtbaR5Uw1TGlTk3qifeGfXDRkQzUvzPEFKAWIqm6hIAjzJQfim5EBbPk5f-Ea-PfU0_uUv9Pr9mEFOqBcXiyTNrTiIRf7Zo9w308YEU4Y3YH0lwTBu4xz-5MPcCkQjWmacFKbxgfzzkPJ7R1adxQ3yJCHrw'
CASTING_DIRECTOR_CREDENTIALS='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii13c29yTGJuU3ZkVnZoc1BNeEdDMiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LXN2LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZmNkMDlmYjRlMmFkMTAwNzE1ZDRhNzUiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjA3MzE2OTkyLCJleHAiOjE2MDc0MDMzOTIsImF6cCI6IkxzN0tqT3pBd0pJTFBwVUplbE13MGhoZVRKSzE3bFlBIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.Xi-iJlPcM8q_p0tsD2R4yMX_b7qMfar2h8iBnpV1EmC60lpxitD44Dz5qOcDqre5BULuK_Iig2EuCfAzJEowB4X21GT6SshH6WZRZJYVHLHmThGsSVGjKIMsJvrlOQw24_AkIk59QjMgeS0YCACY9yo0Og5JssrnotVMU2MZpSeiDSJwivGE76H1iIT0TmimvZHN22J0KLu-g3Hk5Sy0YDvr38uhJnEtlbQUJHjvkxaCarpQef1Qhqq5RW6rFlxjeEOswpKWOcWkSvMPrAKcN4V17Aymkl8rvJmo1ECuUbOzKQxB5dFij_gSJrOtqDLPJXQFCogr11vq80DKpzFLqg'
CASTING_ASSISTANT_CREDENTIALS='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii13c29yTGJuU3ZkVnZoc1BNeEdDMiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LXN2LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZmNkMGExNDRlMmFkMTAwNzE1ZDRhOWUiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjA3MzE3MTE1LCJleHAiOjE2MDc0MDM1MTUsImF6cCI6IkxzN0tqT3pBd0pJTFBwVUplbE13MGhoZVRKSzE3bFlBIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.pC9YgBAfMArJTNfwiwbKtFEO9oGjYbRbLABTbThvH_Iq_uEb2cyxzXcWTNfG2o1ljbcC23sfVRY_jYXQywvEI_XBWqcJlrZYhLT_AGRAwTLh4KpYdvAac8X89hx3Zj0r5VPXf51PzUA3B_fipndUZT9bcoiJizpdpFfDeOtYt_wrGii73-8Zt47-XVAVVAPt0FfbyLeHjpfejSQkEWj7dEjRJ5l9C8ZArRbn96zD24msc9ustu9PZb4ZRWjSDhQD8_R9KYz3FqDOrdjaE9ZLaJibjCYowhth-4nmbbBZTe2H71lboSMRblYXaUdV7xNb--Cuh2IBVmxlFiI-QnkD-g'



class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client =self.app.test_client
        # self.database_name = "casting_agency"
        # self.database_path = "postgres://{}/{}".format('suresh:fsd@localhost:5432', self.database_name)
        self.database_path = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
    
    def tearDown(self):
        pass
  

    def test_get_all_movies(self):
        res = self.client().get('/movies', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movies'])


    def test_get_movie(self):
        res = self.client().get('/movies/1', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie'])


    def test_get_movie_not_found(self):
        res = self.client().get('/movies/10', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data['success'], False)


    def test_post_movies(self):
        res = self.client().post('/movies', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)}, 
        json={"release_date": "01-01-2018","title": "Ant Man"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['movie'])
        self.assertTrue(len(data['movie']))


    def test_post_movies_bad_request(self):
        res = self.client().post('/movies', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(data['success'], False)


    def test_delete_movies(self):
        res = self.client().delete('/movies/3', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)


    def test_delete_movies_not_found(self):
        res = self.client().delete('/movies/100', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data['success'], False)


    def test_patch_movies(self):
        res = self.client().patch('/movies/2', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)},
        json={"title": "Avengers-EG", "release_date": "2018-01-01"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie'])
        self.assertTrue(data['success'], True)


    def test_patch_movies_bad_request(self):
        res = self.client().patch('/movies/2', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(data['success'], False)


    def test_patch_movies_invalid_id(self):
        res = self.client().patch('/movies/25', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)},
        json={"title": "Avengers-EP", "release_date": "2018-01-01"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data['success'], False)


    def test_get_movie_casting_director(self):
        res = self.client().get('/movies/1', headers={"Authorization": "Bearer {}".format(CASTING_DIRECTOR_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie'])


    def test_patch_movies_casting_director(self):
        res = self.client().patch('/movies/2', headers={"Authorization": "Bearer {}".format(CASTING_DIRECTOR_CREDENTIALS)},
        json={"title": "Avengers-CD1", "release_date": "2018-01-01"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie'])
        self.assertTrue(data['success'], True)


    def test_401_post_movie_unauthorized_casting_director(self):
        res = self.client().post('/movies', headers={"Authorization": "Bearer {}".format(CASTING_DIRECTOR_CREDENTIALS)}, 
        json={"release_date": "01-01-2018","title": "SpiderMan-CD"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')


    def test_get_movie_casting_assistant(self):
        res = self.client().get('/movies/1', headers={"Authorization": "Bearer {}".format(CASTING_ASSISTANT_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie'])


    def test_patch_movies_casting_director(self):
        res = self.client().patch('/movies/2', headers={"Authorization": "Bearer {}".format(CASTING_ASSISTANT_CREDENTIALS)},
        json={"title": "Avengers-CD1", "release_date": "2018-01-01"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')


    def test_401_post_movie_unauthorized_casting_director(self):
        res = self.client().post('/movies', headers={"Authorization": "Bearer {}".format(CASTING_ASSISTANT_CREDENTIALS)}, 
        json={"release_date": "01-01-2018","title": "SpiderMan-CD"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')


    def test_delete_movies(self):
        res = self.client().delete('/movies/7', headers={"Authorization": "Bearer {}".format(CASTING_ASSISTANT_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')


    def test_get_actors(self):
        res = self.client().get('/actors', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actors'])
        

    def test_get_actor(self):
        res = self.client().get('/actors/2', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actor'])


    def test_get_actor_not_found(self):
        res = self.client().get('/actors/100', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data['success'], False)


    def test_post_actors(self):
        res = self.client().post('/actors', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)},
        json={"age": 35,"gender": "female","name": "Elizabeth Olsen"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)


    def test_post_actors_bad_request(self):
        res = self.client().post('/actors', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(data['success'], False)


    def test_delete_actors(self):
        res = self.client().delete('/actors/3', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)


    def test_delete_actors_not_found(self):
        res = self.client().delete('/actors/25', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data['success'], False)


    def test_patch_actors(self):
        res = self.client().patch('/actors/2', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)},
        json={"age": 45, "gender": "female", "name": "Chris Evans"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)


    def test_patch_actors_bad_request(self):
        res = self.client().patch('/actors/25', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(data['success'], False)


    def test_get_actor_casting_director(self):
        res = self.client().get('/actors/2', headers={"Authorization": "Bearer {}".format(CASTING_DIRECTOR_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actor'])


    def test_patch_actors_casting_director(self):
        res = self.client().patch('/actors/2', headers={"Authorization": "Bearer {}".format(CASTING_DIRECTOR_CREDENTIALS)},
        json={"age": 45, "gender": "male", "name": "Chris Evans"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)

    def test_get_actor_casting_assistant(self):
        res = self.client().get('/actors/2', headers={"Authorization": "Bearer {}".format(CASTING_ASSISTANT_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actor'])


    def test_patch_actors_casting_assistant(self):
        res = self.client().patch('/actors/8', headers={"Authorization": "Bearer {}".format(CASTING_ASSISTANT_CREDENTIALS)},
        json={"age": 45, "gender": "female", "name": "Kate Win"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')


    def test_delete_actors_casting_assistant(self):
        res = self.client().delete('/actors/25', headers={"Authorization": "Bearer {}".format(CASTING_ASSISTANT_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')


if __name__ == "__main__":
    unittest.main()