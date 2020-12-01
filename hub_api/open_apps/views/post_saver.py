import logging
from datetime import date
from random import random

from django.db import IntegrityError
from fuzzywuzzy import process
from open_apps.authentication import FirebaseAuthentication
from open_apps.models.post_saver import Post, SavedPost, Title
from open_apps.permissions import IsOwnerOrReadOnly
from open_apps.serializers.post_saver import (PostSerializer,
                                              SavedPostSerializer,
                                              TitleSerializer)
from rest_framework import permissions, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

logger = logging.getLogger(__file__)

is_authenticated_and_owner_classes = [
    permissions.IsAuthenticated, IsOwnerOrReadOnly]


class NormalResultsSetPagination(PageNumberPagination):
    page_size = 30


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` actions.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, FirebaseAuthentication]
    pagination_class = NormalResultsSetPagination

    def get_queryset(self):
        return Post.objects.filter(date=date.today()).order_by('id')

    def retrieve(self, request, pk=None):
        response = {'message': 'Detail function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `update`, and `destroy` actions.
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
    This viewset automatically provides `list` actions.
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
                        try:
                            SavedPost.objects.get_or_create(
                                title=f"{posts[index].title}{str(random())[0:5]}", url=posts[index].url, user=self.request.user)
                        except:
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
