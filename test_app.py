import os
import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
from unittest.mock import patch

from app import create_app
from models import setup_db, Actor, Movie


EXECUTIVE_PRODUCER = os.environ.get(
    'EXECUTIVE_PRODUCER_CREDENTIALS')
CASTING_DIRECTOR = os.environ.get(
    'CASTING_DIRECTOR_CREDENTIALS')
CASTING_ASSISTANT = os.environ.get(
    'CASTING_ASSISTANT_CREDENTIALS')


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def tearDown(self):
        pass

    def test_get_all_movies(self):
        res = self.client().get(
            '/movies',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movies'])

    def test_get_movie(self):
        res = self.client().get(
            '/movies/1',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie'])

    def test_get_movie_not_found(self):
        res = self.client().get(
            '/movies/10',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(res.data)

        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data['success'], False)

    def test_post_movies(self):
        res = self.client().post(
            '/movies',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER},
            json={"release_date": "01-01-2018", "title": "Ant Man"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['movie'])
        self.assertTrue(len(data['movie']))

    def test_post_movies_bad_request(self):
        res = self.client().post(
            '/movies',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(res.data)

        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(data['success'], False)

    def test_delete_movies(self):
        res = self.client().delete(
            '/movies/3',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)

    def test_delete_movies_not_found(self):
        res = self.client().delete(
            '/movies/100',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(res.data)

        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data['success'], False)

    def test_patch_movies(self):
        res = self.client().patch(
            '/movies/2',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER},
            json={"title": "Avengers-EG", "release_date": "2018-01-01"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie'])
        self.assertTrue(data['success'], True)

    def test_patch_movies_bad_request(self):
        res = self.client().patch(
            '/movies/2',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(res.data)

        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(data['success'], False)

    def test_patch_movies_invalid_id(self):
        res = self.client().patch(
            '/movies/25',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER},
            json={"title": "Avengers-EP", "release_date": "2018-01-01"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data['success'], False)

    def test_get_movie_casting_director(self):
        res = self.client().get(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie'])

    def test_patch_movies_casting_director(self):
        res = self.client().patch(
            '/movies/2',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR},
            json={"title": "Avengers-CD1", "release_date": "2018-01-01"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie'])
        self.assertTrue(data['success'], True)

    def test_401_post_movie_unauthorized_casting_director(self):
        res = self.client().post(
            '/movies',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR},
            json={"release_date": "01-01-2018", "title": "SpiderMan-CD"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_get_movie_casting_assistant(self):
        res = self.client().get(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie'])

    def test_patch_movies_casting_director(self):
        res = self.client().patch(
            '/movies/2',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT},
            json={"title": "Avengers-CD1", "release_date": "2018-01-01"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_401_post_movie_unauthorized_casting_director(self):
        res = self.client().post(
            '/movies',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT},
            json={"release_date": "01-01-2018", "title": "SpiderMan-CD"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_delete_movies(self):
        res = self.client().delete(
            '/movies/7',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_get_actors(self):
        res = self.client().get(
            '/actors',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actors'])

    def test_get_actor(self):
        res = self.client().get(
            '/actors/2',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actor'])

    def test_get_actor_not_found(self):
        res = self.client().get(
            '/actors/100',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(res.data)

        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data['success'], False)

    def test_post_actors(self):
        res = self.client().post(
            '/actors',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER},
            json={"age": 35, "gender": "female", "name": "Elizabeth Olsen"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)

    def test_post_actors_bad_request(self):
        res = self.client().post(
            '/actors',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(res.data)

        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(data['success'], False)

    def test_delete_actors(self):
        res = self.client().delete(
            '/actors/3',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)

    def test_delete_actors_not_found(self):
        res = self.client().delete(
            '/actors/25',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(res.data)

        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data['success'], False)

    def test_patch_actors(self):
        res = self.client().patch(
            '/actors/2',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER},
            json={"age": 45, "gender": "female", "name": "Chris Evans"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)

    def test_patch_actors_bad_request(self):
        res = self.client().patch(
            '/actors/25',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(res.data)

        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(data['success'], False)

    def test_get_actor_casting_director(self):
        res = self.client().get(
            '/actors/2',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actor'])

    def test_patch_actors_casting_director(self):
        res = self.client().patch(
            '/actors/2',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR},
            json={"age": 45, "gender": "male", "name": "Chris Evans"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)

    def test_get_actor_casting_assistant(self):
        res = self.client().get(
            '/actors/2',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actor'])

    def test_patch_actors_casting_assistant(self):
        res = self.client().patch(
            '/actors/8',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT},
            json={"age": 45, "gender": "female", "name": "Kate Win"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_delete_actors_casting_assistant(self):
        res = self.client().delete(
            '/actors/25',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')


if __name__ == "__main__":
    unittest.main()
