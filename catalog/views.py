from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet

from catalog import serializers
from catalog.models import Book, UserBookRelation


class BookViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    filterset_fields = ('genre__name', 'author__fullname')

    def get_queryset(self):
        return Book.objects \
            .prefetch_reviews() \
            .annotate_avg_rating() \
            .annotate_is_saved(user=self.request.user)

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'list':
            return serializers.BookShortSerializer
        elif self.action == 'retrieve':
            return serializers.BookSerializer


class UserBookRelationViewSet(mixins.UpdateModelMixin, GenericViewSet):
    queryset = UserBookRelation.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.RateBookSerializer
    lookup_field = 'book_id'

    def get_object(self):
        obj, _ = UserBookRelation.objects.get_or_create(user_id=self.request.user.id,
                                                        book_id=self.kwargs['book_id'])
        return obj

    def get_serializer_class(self):
        if self.action == 'rate':
            return serializers.RateBookSerializer
        elif self.action == 'save':
            return serializers.SaveBookSerializer

    @action(detail=True, methods=['put'])
    def rate(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @action(detail=True, methods=['put'])
    def save(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # hide methods below in swagger
    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
