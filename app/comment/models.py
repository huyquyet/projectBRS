from django.db import models

# Create your models here.
from django.utils import timezone
from swampdragon.models import SelfPublishModel
# from app.book.serializers import MoreCommentSerializer
from app.review.models import Review
from app.user.models import UserProfile


class CommentReview(SelfPublishModel, models.Model):
    # serializer_class = MoreCommentSerializer
    review = models.ForeignKey(Review, related_name='comment')
    user_profile = models.ForeignKey(UserProfile, related_name='comment_review')
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'comment_review'

    def get_total_like(self):
        return LikeComment.objects.filter(comment=self).count()


class LikeComment(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='like_comment_user')
    comment = models.ForeignKey(CommentReview, related_name='like_comment')
    date = models.DateTimeField(default=timezone.now)
