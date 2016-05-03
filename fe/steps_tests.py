


import os
import steps
import unittest
import tempfile
import db

class ApiTestCase(unittest.TestCase):


    def setUp(self):
	config = steps.read_config("tests-config.yml")
	steps.db_conn = db.open_connection(config["db"])
        self.app = steps.app.test_client()

      
    def test_01_first(self):
        steps.empty_db(steps.db_conn)

    def test_02_root(self):
        rv = self.app.get("/")
        assert "Hello World!" in rv.data


    def test_03_post_steps_missing_parms(self):
        rv = self.app.post("/v1/steps")
        assert "Missing" in rv.data
    
    def test_04_post_steps_missing_component(self):
        rv = self.app.post("/v1/steps?status=s1&owner=o1" \
            "&version=1.025")
        assert "Missing component" in rv.data
       
    def test_05_post_steps_missing_status(self):
        rv = self.app.post("/v1/steps?component=c1&owner=o1" \
            "&version=1.025")
        assert "Missing status" in rv.data
       
    def test_06_post_steps_missing_version(self):
        rv = self.app.post("/v1/steps?status=s1&owner=o1" \
            "&component=s2")
        assert "Missing version" in rv.data
    
    def test_07_post_steps_ok(self):
        rv = self.app.post("/v1/steps?status=s1&owner=test-owner" \
            "&component=s2&version=v1")
        assert "201" in rv.status
    
    def test_08_get_invalid_date(self):
        rv = self.app.get("/v1/steps?start_datetime=2015-20-11%2013%3A00%3A00")
        assert "400" in rv.status
        assert "Datetimes must follow" in rv.data

    def test_09_get_by_owner(self):
        rv = self.app.get("/v1/steps?owner=test-owner")
        assert "200" in rv.status
        assert "test-owner" in rv.data      
    
    def test_10_get(self):
        rv = self.app.get("/v1/steps")
        assert "200" in rv.status
      

#class FlaskrTestCase(unittest.TestCase):


       
       
if __name__ == '__main__':

    unittest.main()




"""
POST /v1/steps
- missing parameters
- exceding parameters?
- mock db_save_step (db_conn,values)


GET /v1/steps
-


valid_date_format (string)


get_where_clause(request<-???)

csv_format(cursor<--???)


db_save_step(conn, step_data(dict)) <- ???

verify_parameters(request, list-parameters(dict)) <--???

"""

