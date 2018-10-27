from rest_framework.pagination import PageNumberPagination


class RecentMatchesPagination(PageNumberPagination):
    page_size = 20
