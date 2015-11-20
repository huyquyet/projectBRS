from django import template
from django.shortcuts import get_object_or_404

from comment.models import CommentReview
from review.models import Review

__author__ = 'FRAMGIA\nguyen.huy.quyet'

register = template.Library()


@register.assignment_tag
def return_user_like_of_comment(comment_id):
    comment = get_object_or_404(CommentReview, pk=comment_id)
    all_user_like_comment = comment.like_comment.all().values_list('user_profile__user__id', flat=True)
    # all_user_like_comment= all_like_comment
    return all_user_like_comment


@register.assignment_tag
def return_comment_of_review(id_review, count):
    number_comment = CommentReview.objects.filter(review=Review.objects.get(id=id_review)).count()
    if number_comment < count:
        comments = CommentReview.objects.filter(review=Review.objects.get(id=id_review))[0:number_comment]
    else:
        comments = CommentReview.objects.filter(review=Review.objects.get(id=id_review))[
                   number_comment - count:number_comment]
    return comments


@register.assignment_tag
def return_number_total_comment(id_review):
    result = CommentReview.objects.filter(review=Review.objects.get(id=id_review)).count()
    return result
