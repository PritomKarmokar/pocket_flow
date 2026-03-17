# Django Imports
from django.urls import path

# Module Imports
from authentication.views.google import GoogleOauthInitiateAPIView

urlpatterns = [
    path('google/login/', GoogleOauthInitiateAPIView.as_view(), name='google_login_initiate'),
]