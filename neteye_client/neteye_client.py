from typing import Any, Dict, Optional

from neteye_client.base import RestClient
from neteye_client.node.node import node
from neteye_client.interface.interface import interface
from neteye_client.arp.arp import arp
from neteye_client.serial.serial import serial
from neteye_client.cable.cable import cable


class NeteyeClient(RestClient):
    """A client for the Neteye API."""
    def __init__(self, url: str):
        """Initialize the Neteye client.

        Args:
            url: The base URL for the Neteye API.
        """
        super().__init__(url)
        self._current_user: Optional[Dict[str, Any]] = None

        # API Resource clients
        self.node = node(self)
        self.interface = interface(self)
        self.arp = arp(self)
        self.serial = serial(self)
        self.cable = cable(self)

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login with email and password to create a session."""
        user_data = self.login_session(json={"email": email, "password": password})
        self._current_user = user_data
        return user_data

    def logout(self) -> Any:
        """Logout the current user and clear the session."""
        response = self.logout_session()
        self._current_user = None
        return response

    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get the currently authenticated user's information."""
        if not self._current_user:
            try:
                self._current_user = self.get("/api/auth/me")
            except Exception:  # Could be APIError or another request exception
                pass  # User is not logged in
        return self._current_user

    def is_authenticated(self) -> bool:
        """Check if the client is currently authenticated."""
        return self.get_current_user() is not None
