from django.db.models import Avg

from django.views.generic.base import ContextMixin

from book.models import Book
from category.models import Category

__author__ = 'FRAMGIA\nguyen.huy.quyet'


class BaseView(ContextMixin):
    model = Book

    def get_context_data(self, **kwargs):
        ctx = super(BaseView, self).get_context_data(**kwargs)
        ctx['base_list_book'] = return_list_book()
        ctx['base_list_category'] = return_list_category()
        return ctx


def return_list_book():
    book = Book.objects.annotate(Avg('rating_book__rate')).order_by('-rating_book__rate__avg')[0:6]
    for i in book:
        i.rate = i.get_rating_book()
        i.count_review = i.review_book.all().count()
    return book


def return_list_category():
    cate = Category.objects.all()
    return cate
