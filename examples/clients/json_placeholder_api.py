import requests


class JsonPlaceholderClient:
    """
    Often APIs are wrapped in a client class, similar to this example
    """
    base_url = "https://jsonplaceholder.typicode.com"

    def get_todo(self, todo_id: int):
        response = requests.get(f"{self.base_url}/todos/{todo_id}")
        response.raise_for_status()
        return response.json()

    def list_all(self):
        response = requests.get(f"{self.base_url}/todos")
        response.raise_for_status()
        return response.json()
