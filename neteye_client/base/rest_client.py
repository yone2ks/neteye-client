import requests
from urllib.parse import urljoin
from typing import Any, Dict, Optional

class APIError(Exception):
    """Custom exception for API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.status_code:
            return f"[Status Code: {self.status_code}] {self.message}"
        return self.message

class RestClient:
    """A base REST client for making API requests."""
    def __init__(self, base_url: str, timeout: int = 10):
        """Initialize the REST client.

        Args:
            base_url: The base URL for the API.
            timeout: The request timeout in seconds.
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.session = requests.Session()
        self.session.headers.update(headers)

    def _handle_response(self, response: requests.Response) -> Any:
        """Handle API responses, checking for errors and parsing the body."""
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                error_data = response.json()
                message = error_data.get("message", str(e))
            except requests.exceptions.JSONDecodeError:
                message = str(e)
            raise APIError(message, status_code=response.status_code)

        if response.status_code == 204:  # No Content
            return None

        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return response.text

    # --- Authentication helpers ---
    def clear_auth(self) -> None:
        """Remove Authorization header and requests auth from the session."""
        self.session.headers.pop("Authorization", None)
        self.session.auth = None

    def login_session(self, path: str = "/api/auth/login", data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None) -> Any:
        """Perform a session login."""
        url = urljoin(self.base_url, path)
        response = self.session.post(url, data=data, json=json, timeout=self.timeout)
        return self._handle_response(response)

    def logout_session(self, path: str = "/api/auth/logout") -> Any:
        """Perform a session logout."""
        url = urljoin(self.base_url, path)
        response = self.session.post(url, timeout=self.timeout)
        self.clear_auth()
        return self._handle_response(response)

    # --- HTTP methods ---
    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Perform a GET request."""
        url = urljoin(self.base_url, path)
        response = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(response)

    def post(self, path: str, data: Optional[Dict[str, Any]] = None) -> Any:
        """Perform a POST request."""
        url = urljoin(self.base_url, path)
        response = self.session.post(url, json=data, timeout=self.timeout)
        return self._handle_response(response)

    def put(self, path: str, data: Dict[str, Any]) -> Any:
        """Perform a PUT request."""
        url = urljoin(self.base_url, path)
        response = self.session.put(url, json=data, timeout=self.timeout)
        return self._handle_response(response)

    def delete(self, path: str) -> Any:
        """Perform a DELETE request."""
        url = urljoin(self.base_url, path)
        response = self.session.delete(url, timeout=self.timeout)
        return self._handle_response(response)
