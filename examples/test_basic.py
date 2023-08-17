from unittest import TestCase

import requests

from examples.simulators.google import GoogleSimulator


class TestBasic(TestCase):
    def test_home_page(self):
        # This will use `GoogleSimulator.simulate_home_page` to initialize the corresponding cassette
        with GoogleSimulator("home_page"):
            response = requests.get("https://www.google.com/")
            self.assertEqual(response.status_code, 200)

    def test_search(self):
        # This will use `GoogleSimulator.simulate_search` to initialize the corresponding cassette
        with GoogleSimulator("search"):
            response = requests.get("https://www.google.com/?search=test")
            self.assertEqual(response.status_code, 200)
