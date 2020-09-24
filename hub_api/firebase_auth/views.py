from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from .authentication import FirebaseAuthentication
from .models import Profile
from .serializers import ProfileSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, FirebaseAuthentication]

    def get_queryset(self):
        return User.objects.filter(username=self.request.user)

    def list(self, request):
        user = User.objects.get(username=self.request.user)
        serialized = UserSerializer(user)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        response = {'message': 'Detail function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        response = {'message': 'Detail function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, pk=None):
        response = {'message': 'Detail function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        response = {'message': 'Detail function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ProfileViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    serializer_class = ProfileSerializer
    authentication_classes = [SessionAuthentication, FirebaseAuthentication]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def list(self, request):
        profile = Profile.objects.get(user=self.request.user)
        serialized = ProfileSerializer(profile)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        response = {'message': 'Detail function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=self.request.user)
            profile.apps = self.request.data["apps"]
            profile.save()
            serialized = ProfileSerializer(profile)
            return Response(serialized.data, status=status.HTTP_202_ACCEPTED)
        except Exception:
            raise Http404('Invalid data')
