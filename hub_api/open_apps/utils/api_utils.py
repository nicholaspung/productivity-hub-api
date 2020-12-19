from rest_framework import status
from rest_framework.response import Response


def unused_method():
    response = {'message': 'Detail function is not offered in this path.'}
    return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)
