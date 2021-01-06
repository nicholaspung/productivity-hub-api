import os

import firebase_admin
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from firebase_admin import auth, credentials
from rest_framework import authentication
from rest_framework.authentication import SessionAuthentication

from open_apps.exceptions import FirebaseError, InvalidAuthToken, NoAuthToken
from open_apps.models.firebase_auth import Profile
from open_apps.models.app import App, APPS

User = get_user_model()


cred = credentials.Certificate(
    {
        "type": "service_account",
        "project_id": os.getenv("FIREBASE_PROJECT_ID"),
        "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
        "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
        "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
        "client_id": os.getenv("FIREBASE_CLIENT_ID"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_CERT_URL"),
    }
)

default_app = firebase_admin.initialize_app(cred)


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", None)
        if not auth_header:
            raise NoAuthToken()

        id_token = auth_header.split(" ").pop()
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise InvalidAuthToken() from None

        if not id_token or not decoded_token:
            return (None, None)

        try:
            uid = decoded_token.get("uid")
            email = decoded_token.get("email", None)
            is_anonymous = decoded_token.get(
                'provider_id', None) == 'anonymous'
        except Exception:
            raise FirebaseError() from None

        user, _ = User.objects.get_or_create(username=uid)
        if email and user.email != email:
            user.email = email
            user.save()

        profile, created = Profile.objects.get_or_create(
            user=user)

        if profile.is_anonymous != is_anonymous:
            profile.is_anonymous = is_anonymous
            profile.save()

        if email and not profile.email:
            profile.email = email
            profile.save()

        # Default app added is Habit Tracker (1)
        if created:
            app = App.objects.get(title=APPS[0])
            user.profile.apps.add(app)

        return (user, None)


GeneralAuthentication = [SessionAuthentication, FirebaseAuthentication]
