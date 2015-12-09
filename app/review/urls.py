from django.conf.urls import url

from app.review import views

__author__ = 'FRAMGIA\nguyen.huy.quyet'

urlpatterns = [
    # url(r'^create/(?P<pk>[0-9]+)$', views.ReviewCreateView, name='review_create'),
    url(r'^create$', views.review_create, name='review_create'),
    url(r'^update$', views.review_update, name='review_update'),
    url(r'^delete$', views.review_delete, name='review_delete'),
    url(r'^like', views.review_like, name='review_like'),
    url(r'^unlike', views.review_unlike, name='review_unlike'),
    # url(r'^like_unlike', views.review_like_unlike, name='review_like_unlike'),
]
