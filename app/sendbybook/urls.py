from django.conf.urls import url

from app.sendbybook import views

__author__ = 'FRAMGIA\nguyen.huy.quyet'

urlpatterns = [
    url(r'^book$', views.SendNewBookView, name='send_new_book'),
    url(r'^manager_book$', views.SendBookManagerView, name='send_book_manager'),
    url(r'^detail_book/(?P<pk>[0-9]+)/$', views.SendBookDetailView, name='send_detail_book'),
    url(r'^delete_book/$', views.delete_book, name='send_delete_book'),
]
