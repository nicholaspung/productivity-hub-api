from rest_framework.pagination import PageNumberPagination


class NormalResultsSetPagination(PageNumberPagination):
    page_size = 30
