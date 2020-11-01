import logging
from datetime import date

from django.db import IntegrityError
from firebase_auth.authentication import FirebaseAuthentication
from fuzzywuzzy import process
from rest_framework import permissions, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Post, SavedPost, Title
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer, SavedPostSerializer, TitleSerializer

logger = logging.getLogger(__file__)

is_authenticated_and_owner_classes = [
    permissions.IsAuthenticated, IsOwnerOrReadOnly]


class NormalResultsSetPagination(PageNumberPagination):
    page_size = 30


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, FirebaseAuthentication]
    pagination_class = NormalResultsSetPagination

    def get_queryset(self):
        return Post.objects.filter(date=date.today())

    def retrieve(self, request, pk=None):
        response = {'message': 'Detail function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)


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

    def retrieve(self, request, pk=None):
        response = {'message': 'Detail function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SavedPostViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    serializer_class = SavedPostSerializer
    permission_classes = is_authenticated_and_owner_classes
    authentication_classes = [SessionAuthentication, FirebaseAuthentication]

    def get_queryset(self):
        # This filtering needs to be updated for better efficiency later
        posts = Post.objects.filter(date=date.today())
        posts_titles = [post.title for post in posts]
        titles = Title.objects.filter(user=self.request.user)
        titles = [title.title for title in titles]

        # Can probably be better build algorithm-wise
        for title in titles:
            similars = process.extract(title, posts_titles, limit=5)
            for similar in similars:  # (title_name, accuracy)
                if similar[1] > 80:
                    index = posts_titles.index(similar[0])
                    try:
                        SavedPost.objects.get_or_create(
                            title=posts[index].title, url=posts[index].url, user=self.request.user)
                    except IntegrityError as e:
                        logger.error('This is an error.')
                        continue
                    except:
                        logger.exception('This is an unhandled exception.')
                        continue

        return SavedPost.objects.filter(user=self.request.user, seen=False)

    def perform_create(self, serializer):
        response = {'message': 'Detail function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, pk=None):
        response = {'message': 'Detail function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        response = {'message': 'Detail function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        response = {'message': 'Detail function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)
