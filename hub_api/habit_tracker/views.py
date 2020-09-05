from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.contrib.auth.models import User

from .models import Todo, Habit, Daily
from .serializers import TodoSerializer, HabitSerializer, DailySerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly


is_authenticated_and_owner_classes = [
    permissions.IsAuthenticated, IsOwnerOrReadOnly]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class TodoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    serializer_class = TodoSerializer
    permission_classes = is_authenticated_and_owner_classes

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)


class HabitViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    serializer_class = HabitSerializer
    permission_classes = is_authenticated_and_owner_classes

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)


class DailyViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    serializer_class = DailySerializer
    permission_classes = is_authenticated_and_owner_classes

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'todos': reverse('snippet-list', request=request, format=format),
        'habits': reverse('habit-list', request=request, format=format),
        'dailies': reverse('daily-list', request=request, format=format)
    })
