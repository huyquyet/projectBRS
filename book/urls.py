from django.conf.urls import url

from book import views

__author__ = 'FRAMGIA\nguyen.huy.quyet'

urlpatterns = [
    #######################################################
    #######################################################
    # Book
    url(r'^$', views.BookIndexView, name='book_index'),
    url(r'^(?P<slug>[\w-]+)/$', views.BookDetailView, name='book_detail'),

    ######################################################
    #####################################################
    # Rating

    url(r'^user/rating/$', views.add_rating, name='book_rating'),

    #######################################################
    ######################################################
    # Read book

    url(r'^user/readbook$', views.want_read_book, name='read_book'),

    #######################################################
    ######################################################
    # Favorite book

    url(r'^user/favorite$', views.favorite_book, name='favorite_book'),
]
