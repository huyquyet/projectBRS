from django import template
from django.shortcuts import get_object_or_404

from comment.models import CommentReview

__author__ = 'FRAMGIA\nguyen.huy.quyet'

register = template.Library()


@register.assignment_tag
def return_user_like_of_comment(comment_id):
    comment = get_object_or_404(CommentReview, pk=comment_id)
    all_user_like_comment = comment.like_comment.all().values_list('user_profile__user__id', flat=True)
    # all_user_like_comment= all_like_comment
    return all_user_like_comment
