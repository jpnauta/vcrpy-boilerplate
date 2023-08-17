from unittest import TestCase

from requests import HTTPError

from examples.simulators.json_placeholder_api import JsonPlaceholderSimulator
from examples.clients.json_placeholder_api import JsonPlaceholderClient


class TestAdvanced(TestCase):
    def setUp(self) -> None:
        self.client = JsonPlaceholderClient()

    def test_multiple_simulations_in_one_test(self):
        with JsonPlaceholderSimulator("list_todos"):
            self.client.list_all()
        with JsonPlaceholderSimulator("list_todos"):
            todos = self.client.list_all()

        self.assertEqual(len(todos), 200)

    def test_simulate_intermittent_error(self):
        # This simulation is configured to produce a hard-to-reproduce error
        with JsonPlaceholderSimulator("list_todos_intermittent_error"):
            with self.assertRaises(HTTPError):
                self.client.list_all()

    def test_mock_client_response(self):
        # This simulation uses mocks instead of cassettes
        with JsonPlaceholderSimulator("list_todos_mock"):
            todos = self.client.list_all()

        self.assertEqual(len(todos), 1)
        self.assertEqual(todos[0], {"test": 123})

    def test_mock_http_error(self):
        # This simulation uses mocks instead of cassettes
        with JsonPlaceholderSimulator("list_todos_mock_error"):
            with self.assertRaises(HTTPError):
                self.client.list_all()

    def test_multiple_api_calls(self):
        # This will record/playback 3 API calls using a single cassette
        with JsonPlaceholderSimulator("multiple_todos"):
            for todo_id in range(1, 4):
                self.client.get_todo(todo_id)
