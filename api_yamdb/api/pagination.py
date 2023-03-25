from rest_framework.pagination import PageNumberPagination


class TitlePagination(PageNumberPagination):
    page_size = 5
