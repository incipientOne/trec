import django
from django.test import TestCase
from django.db import models
from trec_eval.trec_wrapper import  trec_wrapper
from trec_eval_project.settings import BASE_DIR
import os.path



# Create your tests here.
class RunningSiteTests(TestCase):
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

class TrecWrapperTests(TestCase):

    def test_trec_eval_returns_MAP_pvalues_rvalues(self):
        data_directory = os.path.join(BASE_DIR, 'pop script data')
        qrel_path = os.path.join(data_directory, 'qrels', 'robust', 'aq.trec2005.qrels.txt')
        run_path = os.path.join(data_directory, 'runs', 'robust', 'aq.trec.bm25.0.50.res.txt')

        mapVal, pMap, rMap = trec_wrapper(qrel_path, run_path)

        self.assertTrue(mapVal != None)
        self.assertTrue(len(pMap) > 0)
        self.assertTrue(len(rMap) > 0)


