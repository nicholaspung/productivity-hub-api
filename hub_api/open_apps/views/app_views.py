from open_apps.models.app import App
from open_apps.serializers.app_serializers import AppSerializer
from rest_framework.generics import ListAPIView


class AppAPIView(ListAPIView):
    """
    This view provides the `list` action.
    """
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = []
    authentication_classes = []
