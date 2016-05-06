
""""
Unit/integration tests. The method names should be self explanatory.
The DB access calls have not been mocked. Instead, we set up a connection
to a test database and we empty it before the tests to make them
predictable.
"""


import unittest
import steps
import db


class ApiTestCase(unittest.TestCase):
    """
    Class to test the API by sending HTTP requests.
    Method names should be self explanatory.
    """

    def setUp(self):
        self.app = steps.app.test_client()

    def test_01_first(self):
        """
        Establishes a connection against the DB (test version) and
        empties it for the upcoming tests. Make sure seresponseer is up by,
        for instance, running
        docker run -p 3306:3306 --name db -e MYSQL_ROOT_PASSWORD=1234567 \
            -d enyamada/steps-db:1.0
        """
        steps.config = steps.read_config("tests-config.yml")
        steps.empty_db(db.open_connection(steps.config["db"]))

    def test_02_root(self):
        response = self.app.get("/")
        assert "Hello World!" in response.data

    def test_03_post_steps_missing_parms(self):
        response = self.app.post("/v1/steps")
        assert "Missing" in response.data

    def test_04_post_steps_missing_component(self):
        response = self.app.post("/v1/steps?status=s1&owner=o1"
                                 "&version=1.025")
        assert "Missing component" in response.data

    def test_05_post_steps_missing_status(self):
        response = self.app.post("/v1/steps?component=c1&owner=o1"
                                 "&version=1.025")
        assert "Missing status" in response.data

    def test_06_post_steps_missing_version(self):
        response = self.app.post("/v1/steps?status=s1&owner=o1"
                                 "&component=s2")
        assert "Missing version" in response.data

    def test_07_post_steps_ok(self):
        response = self.app.post("/v1/steps?status=s1&owner=test-owner"
                                 "&component=s2&version=v1")
        assert "201" in response.status

    def test_08_get_invalid_date(self):
        response = self.app.get("/v1/steps?start_datetime=2015-20-11%2013%3A00%3A00")
        assert "400" in response.status
        assert "Datetimes must follow" in response.data

    def test_09_get_by_owner(self):
        response = self.app.get("/v1/steps?owner=test-owner")
        assert "200" in response.status
        assert "test-owner" in response.data

    def test_10_get(self):
        response = self.app.get("/v1/steps")
        assert "200" in response.status



if __name__ == '__main__':
    unittest.main()


