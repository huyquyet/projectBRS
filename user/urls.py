from django.conf.urls import url

from user import views

__author__ = 'FRAMGIA\nguyen.huy.quyet'

urlpatterns = [
    url(r'^$', views.UserIndexView, name='user_index')
]
