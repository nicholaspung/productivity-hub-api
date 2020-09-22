from rest_framework import permissions, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from firebase_auth.authentication import FirebaseAuthentication

from .models import Post, Title, SavedPost
from .serializers import PostSerializer, TitleSerializer, SavedPostSerializer
from .permissions import IsOwnerOrReadOnly

is_authenticated_and_owner_classes = [
    permissions.IsAuthenticated, IsOwnerOrReadOnly]


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, FirebaseAuthentication]


class TitleViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    serializer_class = TitleSerializer
    permission_classes = is_authenticated_and_owner_classes
    authentication_classes = [SessionAuthentication, FirebaseAuthentication]

    def get_queryset(self):
        return Title.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SavedPostViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    serializer_class = SavedPostSerializer
    permission_classes = is_authenticated_and_owner_classes
    authentication_classes = [SessionAuthentication, FirebaseAuthentication]

    def get_queryset(self):
        return SavedPost.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
