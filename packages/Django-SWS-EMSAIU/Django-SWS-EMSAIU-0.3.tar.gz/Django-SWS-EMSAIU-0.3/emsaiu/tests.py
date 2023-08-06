import json
import unittest

from django.contrib.auth.models import User
from django.test import Client


def get_user(username):
    try:
        user = User.objects.get(username=username)
        return user
    except Exception:
        user = User.objects.create_user(username, password='pass')
        return user


def get_user_pass(username):
    return 'pass'


class AIUTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def set_user(self, username):
        get_user(username)
        self.client.login(username=username,
                          password=get_user_pass(username))

    def test_mainpage(self):
        self.set_user('javerage')

        # Issue a GET request.
        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context matches the mock data.
        self.assertEqual(response.context['term_year'], 2013)
        self.assertEqual(response.context['term_quarter'], 'spring')

    def test_api(self):
        # Issue a GET request.
        response = self.client.get('/api/v1/aiu/2013-spring')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(data['term']['year'], 2013)
        self.assertEquals(data['term']['quarter'], 'Spring')
        self.assertEquals(data['term']['first_day_quarter'], '2013-04-01')

        self.assertEquals(len(data['records']), 4)
