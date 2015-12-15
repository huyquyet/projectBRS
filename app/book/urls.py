from django.conf.urls import url

from app.book import views

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
    url(r'^user/readfinish$', views.read_finish, name='read_finish'),

    #######################################################
    ######################################################
    # Favorite book

    url(r'^user/add_favorite$', views.favorite_book, name='favorite_book'),
    url(r'^user/un_favorite$', views.un_favorite_book, name='un_favorite_book'),

    #######################################
    #######################################
    # User Manager Book

    url(r'^(?P<username>[\w-]+)/book$', views.BookManagerView, name='user_manager_book'),
    url(r'^(?P<username>[\w-]+)/book/read$', views.BookManagerReadView, name='user_manager_book_read'),
    url(r'^(?P<username>[\w-]+)/book/reading$', views.BookManagerReadingView, name='user_manager_book_reading'),
    url(r'^(?P<username>[\w-]+)/book/favorite$', views.BookManagerFavoriteView, name='user_manager_book_favorite'),
]
