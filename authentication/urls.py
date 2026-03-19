# Django Imports
from django.urls import path

# Module Imports
from authentication.views.google import GoogleOauthInitiateAPIView, GoogleCallBackEndPointAPIView

urlpatterns = [
    path(
        'google/login/',
        GoogleOauthInitiateAPIView.as_view(),
        name='google_login_initiate'
    ),

    path(
        'google/callback/',
        GoogleCallBackEndPointAPIView.as_view(),
        name='google_login_callback'
    )
]