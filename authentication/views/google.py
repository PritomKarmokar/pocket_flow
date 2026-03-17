# Python imports
import uuid

# Django imports
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

# Rest Framework Imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

# Module Imports
from applibs.logger import get_logger
from applibs.status.error_code import GOOGLE_OAUTH_INITIATE_FAILED
from services.google_oauth import GoogleOAuthProvider

logger = get_logger(__name__)

class GoogleOauthInitiateAPIView(APIView):
    def get(self, request: Request) -> HttpResponseRedirect | Response:
        try:
            state = uuid.uuid4().hex
            provider = GoogleOAuthProvider(request, state)
            request.session['state'] = state
            auth_url = provider.get_auth_url()
            return redirect(auth_url)
        except Exception as e:
            logger.error(
                "Error Occurred while initiating Google Oauth", str(e)
            )
            return Response(
                GOOGLE_OAUTH_INITIATE_FAILED, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )