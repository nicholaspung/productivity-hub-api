from django.http import Http404
from firebase_admin import auth
from open_apps.authentication import FirebaseAuthentication
from open_apps.models.firebase_auth import Profile, UserAnalytic, ViceThreshold
from open_apps.serializers.firebase_auth import (ProfileSerializer,
                                                 UserAnalyticSerializer,
                                                 UserSerializer)
from open_apps.views.habit_tracker import get_date, week__range
from rest_framework import status, viewsets
from rest_framework.generics import DestroyAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response


class UserViewSet(DestroyAPIView):
    """
    This viewset automatically provides `destroy` actions.
    """
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, FirebaseAuthentication]

    def destroy(self, request, *args, **kwargs):
        firebase_uid = self.request.user.username
        error = None
        try:
            firebase_user = auth.get_user(firebase_uid)
            if firebase_user:
                auth.delete_user(firebase_user.uid)
        except auth.UserNotFoundError as err:
            error = err

        response = super().destroy(self, request, *args, **kwargs)

        if error is not None:
            response = {'error': error.default_message}
        return response


class ProfileViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `update` actions.
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

    def create(self, request, pk=None):
        response = {'message': 'Detail function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        response = {'message': 'Detail function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UserAnalyticViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, and `retrieve` actions.
    """
    serializer_class = UserAnalyticSerializer
    authentication_classes = [SessionAuthentication, FirebaseAuthentication]

    def get_queryset(self):
        return UserAnalytic.objects.get(user=self.request.user)

    def list(self, request):
        '''
        timezone = self.request.headers['Timezone']
        '''
        obj_date = get_date(self.request.query_params)  # 2020-10-10
        isocalendar = obj_date.isocalendar()
        week_dates = week__range(obj_date.year, isocalendar)
        queryset = UserAnalytic.objects.filter(user=self.request.user, date__range=(
            week_dates[0], week_dates[1])).order_by('id')
        serialized = UserAnalyticSerializer(queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request, pk=None):
        def increment_frequency(obj):
            obj.frequency += 1
            obj.save()

        obj_date = get_date(self.request.query_params)  # 2020-10-10
        label_request = self.request.data.get('label', False)

        if label_request:
            obj, created = UserAnalytic.objects.get_or_create(
                user=self.request.user, label=label_request, date=obj_date)
            if not created:
                increment_frequency(obj)
            return Response({'message': 'Analytics created.'}, status=status.HTTP_201_CREATED)
        else:
            try:
                labels = ["Post Saver Nav", "Saved Post Title",
                          "Saved Post Refresh", "All Post Title", "All Post Refresh"]
                for label in labels:
                    try:
                        user_analytic_threshold = ViceThreshold.objects.filter(
                            user=self.request.user, label=label)[0]
                        UserAnalytic.objects.get_or_create(
                            user=self.request.user, label=label, date=obj_date, threshold=user_analytic_threshold)
                    except:
                        filtered_user_analytics = UserAnalytic.objects.filter(
                            user=self.request.user, label=label)
                        number_of_user_analytic_for_label = len(
                            filtered_user_analytics)
                        if number_of_user_analytic_for_label > 7:
                            average_frequency_of_user_analytic = sum(
                                [analytic.frequency for analytic in filtered_user_analytics])//number_of_user_analytic_for_label
                            if average_frequency_of_user_analytic < 5:
                                average_frequency_of_user_analytic = 5
                            try:
                                ViceThreshold.objects.get_or_create(
                                    user=self.request.user, label=label, threshold=average_frequency_of_user_analytic)
                            except:
                                pass
                        UserAnalytic.objects.get_or_create(
                            user=self.request.user, label=label, date=obj_date)
                return Response({'message': 'Analytics created.'}, status=status.HTTP_201_CREATED)
            except Exception:
                raise Http404('Something went wrong.')

    def partial_update(self, request, pk=None):
        response = {'message': 'Detail function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        response = {'message': 'Detail function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)
