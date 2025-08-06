import requests
import  time

class OpenLibraryAPIClient:
    BASE_URL="https://openlibrary.org"

    def __init__(self, rate_limit_seconds: float = 1.0):
        self.rate_limit_seconds = rate_limit_seconds
        self.last_request_time = 0

    def get(self, endpoint: str, params: dict = None) -> dict:
        self._respect_rate_limit()
        url = self.BASE_URL + endpoint
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed: {response.status_code}")

    def _respect_rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit_seconds:
            time.sleep(self.rate_limit_seconds - elapsed)
        self.last_request_time = time.time()