from rest_framework.pagination import PageNumberPagination


class ProductPageNumberPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 6
