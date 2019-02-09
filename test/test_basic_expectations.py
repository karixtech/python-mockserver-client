import requests
from mockserver import request, response, times, seconds, timesrange
from test import MOCK_SERVER_URL, MockServerClientTestCase


class TestBasicExpectations(MockServerClientTestCase):
    def test_expect_once_not_called_fails(self):
        self.client.expect(
            request(),
            response(),
            times(1)
        )

        with self.assertRaises(AssertionError):
            self.client.verify_expectations()

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

    def test_expect_never(self):
        self.client.expect(
            request(),
            response(),
            times(0)
        )

        self.client.verify_expectations()

    def test_expect_never_fails(self):
        self.client.expect(
            request(),
            response(),
            times(0)
        )

        result = requests.get(MOCK_SERVER_URL + "/path")
        self.assertEqual(result.status_code, 404)

        with self.assertRaises(AssertionError):
            self.client.verify_expectations()

    def test_expect_no_range(self):
        self.client.expect(
            request(),
            response(),
            timesrange()
        )

        result = requests.get(MOCK_SERVER_URL + "/path")
        self.assertEqual(result.status_code, 200)

        self.client.verify_expectations()

    def test_expect_atleast_once(self):
        self.client.expect(
            request(),
            response(),
            timesrange(atleast=1)
        )

        result = requests.get(MOCK_SERVER_URL + "/path")
        self.assertEqual(result.status_code, 200)

        result = requests.get(MOCK_SERVER_URL + "/path")
        self.assertEqual(result.status_code, 200)

        self.client.verify_expectations()

    def test_expect_atleast_twice_fails(self):
        self.client.expect(
            request(),
            response(),
            timesrange(atleast=2)
        )

        result = requests.get(MOCK_SERVER_URL + "/path")
        self.assertEqual(result.status_code, 200)

        with self.assertRaises(AssertionError):
            self.client.verify_expectations()

    def test_expect_atmost_once(self):
        self.client.expect(
            request(),
            response(),
            timesrange(atmost=1)
        )

        result = requests.get(MOCK_SERVER_URL + "/path")
        self.assertEqual(result.status_code, 200)

        self.client.verify_expectations()

    def test_expect_atmost_once_fails(self):
        self.client.expect(
            request(),
            response(),
            timesrange(atmost=1)
        )

        result = requests.get(MOCK_SERVER_URL + "/path")
        self.assertEqual(result.status_code, 200)

        result = requests.get(MOCK_SERVER_URL + "/path")
        self.assertEqual(result.status_code, 404)

        with self.assertRaises(AssertionError):
            self.client.verify_expectations()

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
