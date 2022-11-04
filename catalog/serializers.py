from rest_framework import serializers

from accounts.serializers import UserShortSerializer
from catalog import models


class BookReviewSerializer(serializers.ModelSerializer):
    user = UserShortSerializer()

    class Meta:
        model = models.UserBookRelation
        fields = ('id', 'user', 'rating', 'note')


class BookShortSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    genre = serializers.CharField(source='genre.name')
    author = serializers.CharField(source='author.fullname')
    avg_rating = serializers.FloatField()
    is_saved = serializers.BooleanField()

    class Meta:
        model = models.Book
        fields = ('id', 'name', 'genre', 'author', 'avg_rating', 'is_saved')


class BookSerializer(BookShortSerializer):
    reviews = BookReviewSerializer(many=True)

    class Meta:
        model = models.Book
        fields = BookShortSerializer.Meta.fields + ('description', 'publish_date', 'reviews')


class RateBookSerializer(serializers.ModelSerializer):
    rating = serializers.ChoiceField(choices=models.UserBookRelation.RATING_CHOICES, allow_null=False)
    book = serializers.CharField(source='book.name', read_only=True)

    class Meta:
        model = models.UserBookRelation
        fields = ('rating', 'note', 'book')


class SaveBookSerializer(serializers.ModelSerializer):
    saved = serializers.BooleanField(allow_null=False)
    book = serializers.CharField(source='book.name', read_only=True)

    class Meta:
        model = models.UserBookRelation
        fields = ('saved', 'book')
