from django.conf.urls import url
from comment import views

__author__ = 'FRAMGIA\nguyen.huy.quyet'

urlpatterns = [
    url(r'^create_comment$', views.comment_create, name='comment_create'),
    url(r'^comment_unlike/$', views.comment_review_unlike, name='comment_review_like_unlike'),
    url(r'^comment_like/$', views.comment_review_like, name='comment_review_like_unlike'),
    url(r'^comment_like_unlike/$', views.comment_review_like_unlike, name='comment_review_like_unlike'),
    url(r'^comment_delete/$', views.comment_delete, name='comment_delete'),
]
