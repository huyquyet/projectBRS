# from time import timezone

from django.db import models
from django.utils import timezone

from category.models import Category
from projectBRS import settings



# Create your models here.
from user.models import UserProfile


class Book(models.Model):
    title = models.TextField()
    slug = models.SlugField(max_length=200)
    category = models.ForeignKey(Category, related_name='book')
    cover = models.ImageField(upload_to=settings.BOOK_DIR, max_length=255, default='', blank=False)
    description = models.TextField(blank=True, default='')
    author = models.TextField()
    publish = models.TextField()
    page = models.IntegerField()
    price = models.FloatField()
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'book'

    def __unicode__(self):
        return self.title

    def get_rating_book(self):
        rating = Rating.objects.filter(book=self)
        total = rating.count()
        if total == 0:
            return 0
        count = 0
        for i in rating:
            count += i.rate
        return round(count / total)


class Rating(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='rating_user')
    book = models.ForeignKey(Book, related_name='rating_book')
    rate = models.IntegerField(default=0)

    class Meta:
        db_table = 'rating'


class ReadReading(models.Model):
    book = models.ForeignKey(Book, related_name='read_reading_book')
    user_profile = models.ForeignKey(UserProfile, related_name='read_reading_user')
    date = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(default=0)

    """
    0 : user not yet read or reading
    1 : user reading
    2 : user read
    """

    class Meta:
        db_table = 'read_reading'


class Favorite(models.Model):
    book = models.ForeignKey(Book, related_name='favorite_book')
    user_profile = models.ForeignKey(UserProfile, related_name='favorite_user')
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'favorite'
