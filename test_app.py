import os
import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
from unittest.mock import patch

from app import create_app
from models import setup_db, Actor, Movie


EXECUTIVE_PRODUCER_CREDENTIALS='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii13c29yTGJuU3ZkVnZoc1BNeEdDMiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LXN2LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZmNkMDlhNWMwNThmODAwNmY0NTkzYjEiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjA3Mzg1NzA0LCJleHAiOjE2MDc0NzIxMDQsImF6cCI6IkxzN0tqT3pBd0pJTFBwVUplbE13MGhoZVRKSzE3bFlBIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.moKLqEn-8Ryl8ELWpzCdFpDle5eefu7X4JxlvdWzO4CHgyKjVXBr_JYfaUY2CCs5jmRGTBjw8gQP9b3ugc2ihpd-VmNEog-7vdiO4ZKIPDN7hsXQpSeJvmqYLMomknJ9ix05Rf_dzLBWJavNnOzSLxBRVV4iSrn3S45jnBQJL-08ihggS8obiN-TBHcwGAo3xtUoSz-XpG4xVEQ5VxSgRTkTi_viaLSn0qOebM89C0Gkpf-Hxc1bDNiB98txExTJJt_GmdULzNrzYpgzDwz1oRL9j45SEoJJLwF55XXspnWv8s8HoBGaOh-9K7RgsaY4ZLE8w7EHucs_d4kA9FOBSw'
CASTING_DIRECTOR_CREDENTIALS='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii13c29yTGJuU3ZkVnZoc1BNeEdDMiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LXN2LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZmNkMDlmYjRlMmFkMTAwNzE1ZDRhNzUiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjA3Mzg1NzkxLCJleHAiOjE2MDc0NzIxOTEsImF6cCI6IkxzN0tqT3pBd0pJTFBwVUplbE13MGhoZVRKSzE3bFlBIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.rLm23wii3OrYkqnDW3XgOlE04DJDpc-q9P31UaRRYRG2kbbRFkYKKhPw7sLLL-NPxmKdF6gsD81tpKQcVTni3vnAsLrpa8r-4TrPrpYI0UJD_2Xphc8LRt5wNYWqpO5cjC0f5X63RxbdXdbnfn17_H4O2BTELVPVsZtTBH7BAq-aqFUuXt8EsLYz0966zODL_OmCc8JV3HpOESTabuyRWGcmuI9Zfn8K7e4YSLFxBjo7F9_Kbc6TFINYSl1AAvUeEdpn5tRzBMRc506qVkyJ_3xTV4K_5Vq9ZG1pJbqb_-PdKEils3K7OKqxl0g5-aah0r-nqjtbkz4n_Qq_pDzkdA'
CASTING_ASSISTANT_CREDENTIALS='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii13c29yTGJuU3ZkVnZoc1BNeEdDMiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LXN2LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZmNkMGExNDRlMmFkMTAwNzE1ZDRhOWUiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjA3Mzg1ODYwLCJleHAiOjE2MDc0NzIyNjAsImF6cCI6IkxzN0tqT3pBd0pJTFBwVUplbE13MGhoZVRKSzE3bFlBIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.laakN9yqJG99He4uLX4IZShdmvFbxuMlEQQwfv3E-uvtT62dKRCAC6y-vEpSUsRxowgmbfmdoLUzKpgj6Ihkv9uZLzyBkw3sr7Bfe2w71COMFcYrNWSgbOzYQL8KeJpxWcflpZcjE3svq0gCwYXqZcmCkpaBzYHWGMSI1eDVmH5JODFh1qxBtHBZ-bzgfMUMp934BmuYwQKoV8gR2r94i8-VknMI4zrtJi3MGnAOhZobqjOTqGRRVvbu3aVxfIwf22TLQqT37FDSmdyqEHfJyH8zQXAk_cFjfZQswUeBKPuH_QRYCswa-ceW0vZWBdcFZ7e4-A-8XVZna7rTi0UbqA'



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