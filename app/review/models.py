from django.db import models

# Create your models here.
from django.utils import timezone
from app.book.models import Book
from app.user.models import UserProfile


class Review(models.Model):
    book = models.ForeignKey(Book, related_name='review_book')
    user_profile = models.ForeignKey(UserProfile, related_name='review_user')
    content = models.TextField(default='')
    date = models.DateTimeField(default=timezone.now)
    like = models.ManyToManyField(UserProfile, related_name='like_review', through='LikeReview')

    class Meta:
        db_table = 'review'

    def get_total_like(self):
        return LikeReview.objects.filter(review=self).count()


class LikeReview(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='like_review_user')
    review = models.ForeignKey(Review, related_name='like_review')
    date = models.DateTimeField(default=timezone.now)

