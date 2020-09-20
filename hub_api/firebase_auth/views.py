from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework import status

from .authentication import FirebaseAuthentication
from .serializers import UserSerializer, ProfileSerializer
from .models import Profile


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, FirebaseAuthentication]

    def get_queryset(self):
        return User.objects.filter(username=self.request.user)

    def list(self, request):
        response = {'message': 'List function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    serializer_class = ProfileSerializer
    authentication_classes = [SessionAuthentication, FirebaseAuthentication]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def list(self, request):
        response = {'message': 'List function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)
