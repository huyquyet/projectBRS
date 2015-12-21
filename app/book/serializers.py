from rest_framework import serializers
# from swampdragon.serializers.model_serializer import ModelSerializer

from app.book.models import Book
# from app.comment.models import CommentReview

__author__ = 'FRAMGIA\nguyen.huy.quyet'


# class MoreCommentSerializer(ModelSerializer):
#     class Meta:
#         model = CommentReview
#         publish_fields = ['review', 'user_profile', 'content', 'date', ]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('id', 'slug')
        depth = 0
