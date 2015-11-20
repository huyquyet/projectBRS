from django import template

from comment.models import CommentReview
from review.models import Review

__author__ = 'FRAMGIA\nguyen.huy.quyet'

register = template.Library()


@register.assignment_tag
def return_comment_of_review(id_review):
    comments = CommentReview.objects.filter(review=Review.objects.get(id=id_review))[0:5]
    return comments
