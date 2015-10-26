from django.conf.urls import url

from review import views

__author__ = 'FRAMGIA\nguyen.huy.quyet'

urlpatterns = [
    # url(r'^create/(?P<pk>[0-9]+)$', views.ReviewCreateView, name='review_create'),
    url(r'^create$', views.review_create, name='review_create'),
    url(r'^like', views.review_like, name='review_like'),
    url(r'^unlike', views.review_unlike, name='review_unlike'),
]
