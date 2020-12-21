import logging
from datetime import date

from open_apps.authentication import GeneralAuthentication
from open_apps.models.post_saver import Post, SavedPost, Title
from open_apps.pagination import NormalResultsSetPagination
from open_apps.permissions import IsAuthenticatedAndOwner
from open_apps.serializers.post_saver_serializers import (PostSerializer,
                                                          SavedPostSerializer,
                                                          TitleSerializer)
from open_apps.utils.api_utils import unused_method
from open_apps.utils.post_saver_utils import generate_saved_posts
from rest_framework import permissions, viewsets
from rest_framework.generics import ListAPIView

logger = logging.getLogger(__file__)


class PostAPIView(ListAPIView):
    """
    This view provides `list` actions.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = GeneralAuthentication
    pagination_class = NormalResultsSetPagination

    def get_queryset(self):
        return Post.objects.filter(date=date.today()).order_by('id')


class TitleViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create`, `update`, and `destroy` actions.
    """
    serializer_class = TitleSerializer
    permission_classes = IsAuthenticatedAndOwner
    authentication_classes = GeneralAuthentication

    def get_queryset(self):
        return Title.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request):
        return unused_method()

    def partial_update(self, request):
        return unused_method()


class SavedPostViewSet(viewsets.ModelViewSet):
    """
    This view provides `list` and `update` actions.
    """
    serializer_class = SavedPostSerializer
    permission_classes = IsAuthenticatedAndOwner
    authentication_classes = GeneralAuthentication

    def get_queryset(self):
        generate_saved_posts(self, logger)
        return SavedPost.objects.filter(user=self.request.user, seen=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request):
        return unused_method()

    def partial_update(self, request):
        return unused_method()

    def destroy(self, request):
        return unused_method()
