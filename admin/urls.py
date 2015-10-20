from django.conf.urls import url

from admin import views

__author__ = 'FRAMGIA\nguyen.huy.quyet'

urlpatterns = [
    # url(r'^', views.adminIndex),
    url(r'^$', views.AdminIndexView, name='admin_index'),
    url(r'^login/$', views.AdminLoginView, name='admin_login'),
    url(r'^logout/$', views.logout_admin, name='admin_logout'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.AdminProfileView, name='admin_detail_profile'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.AdminEditProfileView, name='admin_edit_profile'),
]
