import requests
from mockserver import request, response, times, seconds
from test import MOCK_SERVER_URL, MockServerClientTestCase


class TestBasicExpectations(MockServerClientTestCase):
    def test_expect_once_called_twice_fails(self):
        self.client.expect(
            request(),
            response(),
            times(1)
        )

        result = requests.get(MOCK_SERVER_URL + "/path")
        self.assertEqual(result.status_code, 200)

        result = requests.get(MOCK_SERVER_URL + "/path")
        self.assertEqual(result.status_code, 404)

    def test_reset_should_clear_expectations(self):
        self.client.expect(
            request(),
            response(),
            times(1)
        )

        self.client.reset()
        self.client.verify_expectations()

    def test_expect_with_ttl(self):
        self.client.expect(
            request(),
            response(),
            times(1),
            seconds(10)
        )
        result = requests.get(MOCK_SERVER_URL + "/path")
        self.assertEqual(result.status_code, 200)
