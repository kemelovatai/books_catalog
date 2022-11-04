from django.contrib import admin
from django.contrib.admin import TabularInline
from . import models


class BookInline(TabularInline):
    model = models.Book
    extra = 0


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = (
        BookInline,
    )


@admin.register(models.BookGenre)
class BookGenreAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(models.UserBookRelation)
class UserBookRelationAdmin(admin.ModelAdmin):
    pass
