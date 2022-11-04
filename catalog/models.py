from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Author(BaseModel):
    fullname = models.CharField(max_length=100, verbose_name=_('Полное имя'), help_text=_('Last name and first name'))
    biography = RichTextField(verbose_name=_('Биография'), null=True, blank=True)

    def __str__(self):
        return f'Id {self.id}: {self.fullname}'


class BookGenre(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_('Название'))
    description = RichTextField(verbose_name=_('Описание'), null=True, blank=True)

    def __str__(self):
        return f'Id {self.id}: {self.name}'


class BookQuerySet(models.QuerySet):
    def prefetch_reviews(self):
        return self.prefetch_related(models.Prefetch(
            'user_relations',
            queryset=UserBookRelation.objects.select_related('user'),
            to_attr='reviews'
        ))

    def annotate_is_saved(self, user):
        return self.annotate(is_saved=models.Exists(UserBookRelation.objects.filter(
                user_id=user.id,
                book_id=models.OuterRef('id'),
                saved=True,
            )))

    def annotate_avg_rating(self):
        return self.annotate(avg_rating=models.Avg('user_relations__rating'))


class Book(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_('Название'))
    author = models.ForeignKey(Author, models.SET_NULL, null=True, blank=True, verbose_name=_('Автор'))
    genre = models.ForeignKey(BookGenre, models.SET_NULL, null=True, blank=True, verbose_name=_('Жанр'))
    description = RichTextField(verbose_name=_('Описание'))
    publish_date = models.DateTimeField()

    objects = BookQuerySet.as_manager()

    def __str__(self):
        return f'Id {self.id}: {self.name}'


class UserBookRelation(BaseModel):
    RATING_CHOICES = (
        (1, 'Terrible'),
        (2, 'Bad'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Great'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_relations')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='user_relations')
    saved = models.BooleanField(default=False)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Id {self.id}: {self.user.email}-{self.book.name}'
