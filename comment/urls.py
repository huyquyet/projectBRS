from django.conf.urls import url
from comment import views

__author__ = 'FRAMGIA\nguyen.huy.quyet'

urlpatterns = [
    url(r'^create_comment$', views.comment_create, name='comment_create'),
]
