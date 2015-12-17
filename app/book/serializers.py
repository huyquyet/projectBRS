from swampdragon.serializers.model_serializer import ModelSerializer
from app.comment.models import CommentReview

__author__ = 'FRAMGIA\nguyen.huy.quyet'


class MoreCommentSerializer(ModelSerializer):
    class Meta:
        model = CommentReview
        publish_fields = ['review', 'user_profile', 'content', 'date', ]
