from django import template

from app.comment import CommentReview

__author__ = 'FRAMGIA\nguyen.huy.quyet'

register = template.Library()


@register.assignment_tag
def return_comment_of_review(id_review):
    comments = CommentReview.objects.filter(review__id=id_review)[0:5]
    return comments
