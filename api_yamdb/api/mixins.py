from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from .permissions import GenreCategoryPermission


class GenreCategoryMixin(viewsets.ModelViewSet):
    permission_classes = (GenreCategoryPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'

    def retrieve(self, request, slug=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, slug=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, slug=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
