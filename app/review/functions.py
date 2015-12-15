from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect

from app.book.models import Book
from app.review.models import Review

__author__ = 'FRAMGIA\nguyen.huy.quyet'


def return_redirect(book_id):
    slug_book = Book.objects.get(pk=book_id).slug
    return HttpResponseRedirect(reverse_lazy("book:book_detail", kwargs={'slug': slug_book}))


def return_list_review_of_user(user):
    list_review = Review.objects.filter(user_profile=user.user_profile).order_by('-date')
    for i in list_review:
        i.point_rating = i.book.get_rating_book()
        i.rating = i.book.rating_book.count()
        i.review = i.book.review_book.count()
        i.number_like_review = i.like_review.all().count()
        i.number_comment_review = i.comment.all().count()
    return list_review
