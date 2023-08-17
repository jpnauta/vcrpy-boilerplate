from requests import HTTPError

from examples.clients.json_placeholder_api import JsonPlaceholderClient
from simulations import BaseSimulator, SimulationFactory


class JsonPlaceholderSimulator(BaseSimulator):
    def simulate_list_todos(self, factory: SimulationFactory):
        factory.use_cassette("jsonplaceholder/list_todos")

    def simulate_multiple_todos(self, factory: SimulationFactory):
        # The cassette for this test will contain multiple request/response pairs
        factory.use_cassette("jsonplaceholder/multiple_todos")

    def simulate_list_todos_intermittent_error(self, factory: SimulationFactory):
        # It is nearly impossible to test intermittent errors, but `raise_http_error_if` can handle this.
        # This simulation will not use any cassettes, and instead return a mock error
        factory.raise_http_error_if(lambda r: '/todos' in r.path, status_code=500)

    def simulate_list_todos_mock(self, factory: SimulationFactory):
        # Sometimes it's necessary to mock certain endpoints. This can be used alongside
        # `use_cassette()` as desired.
        factory.mock_return_value(JsonPlaceholderClient, 'list_all', [{"test": 123}])

    def simulate_list_todos_mock_error(self, factory: SimulationFactory):
        # Sometimes it's necessary to mock certain endpoints. This can be used alongside
        # `use_cassette()` as desired.
        factory.mock_exception(JsonPlaceholderClient, 'list_all', HTTPError("Test error"))
