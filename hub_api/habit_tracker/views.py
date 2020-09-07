from datetime import date

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


def reorder(self, Model, ModelSerializer, id):
    model1 = self.get_object()
    model2 = Model.objects.get(pk=id)

    model1.order, model2.order = model2.order, model1.order

    model1.save()
    model2.save()

    serializer1 = ModelSerializer(model1)
    serializer2 = ModelSerializer(model2)

    return Response([serializer1.data, serializer2.data])


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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        if 'reorder' in request.data:
            return reorder(self, Todo, TodoSerializer, request.data['reorder'])
        else:
            return self.update(request, *args, **kwargs)


class HabitViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    serializer_class = HabitSerializer
    permission_classes = is_authenticated_and_owner_classes

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        if 'reorder' in request.data:
            return reorder(self, Habit, HabitSerializer, request.data['reorder'])
        else:
            return self.update(request, *args, **kwargs)


class DailyViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    serializer_class = DailySerializer
    permission_classes = is_authenticated_and_owner_classes

    def get_queryset(self):
        user = self.request.user
        habits = Habit.objects.filter(user=user)

        for habit in habits:
            Daily.objects.get_or_create(
                habit=habit, date=date.today(), user=user)

        if 'date' in self.request.query_params:
            if self.request.query_params['date'] == 'week':
                queryset = Daily.objects.filter(date__range=())
            elif self.request.query_params['date'] == 'month':
                queryset = Daily.objects.filter(date__range=())
            elif self.request.query_params['date'] == 'year':
                queryset = Daily.objects.filter(date__range=())
            else:
                queryset = Daily.objects.filter(
                    user=self.request.user, date=date.today())
        else:
            queryset = Daily.objects.filter(
                user=self.request.user, date=date.today())

        return queryset


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'todos': reverse('snippet-list', request=request, format=format),
        'habits': reverse('habit-list', request=request, format=format),
        'dailies': reverse('daily-list', request=request, format=format)
    })
