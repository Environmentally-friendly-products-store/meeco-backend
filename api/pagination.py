from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'limit'
