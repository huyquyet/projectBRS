from django.conf.urls import url

from book import views

__author__ = 'FRAMGIA\nguyen.huy.quyet'

urlpatterns = [
    #######################################################
    #######################################################
    # Book
    url(r'^$', views.BookIndexView, name='book_index'),
    url(r'^(?P<slug>[\w-]+)$', views.BookDetailView, name='book_detail'),

    ######################################################
    #####################################################
    # Rating

    url(r'^rating$', views.add_rating, name='book_rating'),
]
