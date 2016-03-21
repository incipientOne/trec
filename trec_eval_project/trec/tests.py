import django
from django.test import TestCase
from django.db import models



# Create your tests here.
class TrecEvalTests(TestCase):
    fixtures = ['test_db.json']

    def setUp(self):
        django.setup()


    def test_core_pages_load(self):
        self.assertEqual(self.client.get("/trec/").status_code, 200)
        self.assertEqual(self.client.get("/trec/users/").status_code, 200)
        self.assertEqual(self.client.get("/trec/tracks/").status_code, 200)
        self.assertEqual(self.client.get("/trec/about/").status_code, 200)
        self.assertEqual(self.client.get("/trec/register/").status_code, 200)
        self.assertEqual(self.client.get("/accounts/login/").status_code, 200)

