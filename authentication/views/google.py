# Python imports
import uuid

# Django imports
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

# Rest Framework Imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# Module Imports
from applibs.logger import get_logger
from applibs.status.error_code import (
    GOOGLE_OAUTH_PROVIDER_ERROR,
    GOOGLE_OAUTH_INITIATE_FAILED,
    GOOGLE_OAUTH_USER_INFO_FETCH_FAILED
)
from applibs.status.success_code import GOOGLE_LOGIN_SUCCESS
from applibs.response import format_output_success
from authentication.models import User, Account
from services.google_oauth import GoogleOAuthProvider

logger = get_logger(__name__)

class GoogleOauthInitiateAPIView(APIView):
    def get(self, request: Request) -> HttpResponseRedirect | Response:
        try:
            state = uuid.uuid4().hex
            provider = GoogleOAuthProvider(request, state)
            request.session['google_oauth_state'] = state
            auth_url = provider.get_auth_url()
            return redirect(auth_url)
        except Exception as e:
            logger.error(
                "Error Occurred while initiating Google Oauth", str(e)
            )
            return Response(
                GOOGLE_OAUTH_INITIATE_FAILED, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GoogleCallBackEndPointAPIView(APIView):
    def get(self, request: Request) -> Response:
        code = request.GET.get('code')
        state = request.GET.get('state')
        saved_state = request.session.pop('google_oauth_state', None)

        if state != saved_state:
            logger.error("State Mismatch for Google OAuth Flow")
            return Response(GOOGLE_OAUTH_PROVIDER_ERROR, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        if not code:
            logger.error("Code is missing in Google OAuth Flow")
            return Response(GOOGLE_OAUTH_PROVIDER_ERROR, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        provider = GoogleOAuthProvider(request)
        token_response = provider.set_token_data(code)
        if not token_response:
            logger.error("Error Occurred while getting User token from Google")
            return Response(GOOGLE_OAUTH_USER_INFO_FETCH_FAILED, status=status.HTTP_400_BAD_REQUEST)

        user_info = provider.get_user_info(token_response['token_type'], token_response['access_token'])
        if not user_info:
            logger.error("Error Occurred while getting User Info from Google")
            return Response(GOOGLE_OAUTH_USER_INFO_FETCH_FAILED, status=status.HTTP_400_BAD_REQUEST)

        email = user_info.get('email')
        with transaction.atomic():
            user, _ = User.objects.get_or_create(email=email)
            user.complete_login_or_signup(user_info)

            Account.objects.update_or_create(
                provider=provider.provider,
                provider_account_id=user_info.get('id'),
                defaults={
                    "user": user,
                    "access_token": token_response['access_token'],
                    "refresh_token": token_response.get('refresh_token'),
                    "id_token": token_response.get('id_token'),
                    "metadata": user_info,
                    "last_connected_at": timezone.now(),
                }
            )

        refresh = RefreshToken.for_user(user)
        response_data = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "header_token": settings.SIMPLE_JWT.get("AUTH_HEADER_TYPES"),
            "expires_in": int(refresh.lifetime.total_seconds()),
            "token_type": "Bearer",
        }
        logger.info({"message": "Google OAuth login successful", "user_id": str(user.id)})
        return Response(
            format_output_success(GOOGLE_LOGIN_SUCCESS,response_data), status=status.HTTP_200_OK
        )