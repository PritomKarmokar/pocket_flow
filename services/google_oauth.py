# Python imports
import requests
from urllib.parse import urlencode
from typing import Optional, Dict, Any

# Django Imports
from django.conf import settings

# Package Imports
from applibs.logger import get_logger

logger = get_logger(__name__)

service_name = settings.SERVICE_NAME

class GoogleOAuthProvider:
    token_url = "https://oauth2.googleapis.com/token"
    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    scope = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
    provider = "google"

    def __init__(self, request, state=None):
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.client_secret = settings.GOOGLE_CLIENT_SECRET
        self.redirect_uri = f"""{"https" if request.is_secure() else "http"}://{request.get_host()}/{service_name}/api/v1/auth/google/callback/"""
        self.url_params = {
            "client_id": self.client_id,
            "scope": self.scope,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "access_type": "offline",
            "prompt": "consent",
            "state": state
        }
        self.auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(self.url_params)}"


    def get_token_url(self) -> str:
        return self.token_url

    def get_auth_url(self) -> str:
        return self.auth_url

    @staticmethod
    def get_headers(token_type: str, token: str) -> Dict[str, Any]:
        headers = {
            "Authorization": f"{token_type} {token}"
        }
        return headers

    def get_user_token(self, data, headers=None) -> Dict[str, Any] | None:
        try:
            headers = headers or {}
            response = requests.post(self.get_token_url(), data=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error("Error Occurred while getting User token from Google", str(e))
            return None

    def set_token_data(self, code: str) -> Dict[str, Any] | None:
        data = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
        }
        token_response = self.get_user_token(data)
        if not token_response:
            logger.error("Error Occurred while getting User token from Google")
            return None

        return token_response

    def get_user_info(self, token_type: str, token: str) -> Dict[str, Any] | None:
        try:
            headers = self.get_headers(token_type, token)
            response = requests.get(url=self.userinfo_url, headers=headers, timeout=settings.REQUEST_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error("Error Occurred while getting User Info from Google:", str(e))
            return None
