from django.conf.urls import url

from admin import views

__author__ = 'FRAMGIA\nguyen.huy.quyet'

urlpatterns = [

    #########################
    ##### Profile
    ########################

    url(r'^$', views.AdminIndexView, name='admin_index'),
    url(r'^login/$', views.AdminLoginView, name='admin_login'),
    url(r'^logout/$', views.logout_admin, name='admin_logout'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.AdminProfileView, name='admin_detail_profile'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.AdminEditProfileView, name='admin_edit_profile'),

    #########################
    ##### Category
    ########################

    url(r'^category$', views.AdminCategoryIndexView, name='admin_category_index'),
    url(r'^category/create$', views.AdminCategoryCreateView, name='admin_category_create'),
    url(r'^category/detail/(?P<slug>[\w-]+)$', views.AdminCategoryDetailView, name='admin_category_detail'),
    url(r'^category/edit/(?P<slug>[\w-]+)$', views.AdminCategoryEditView, name='admin_category_edit'),

    #########################
    ##### Book
    ########################

    url(r'^book$', views.AdminBookIndexView, name='admin_book_index'),
    url(r'^book/create$', views.AdminBookCreateView, name='admin_book_create'),
    url(r'^book/edit/(?P<slug>[\w-]+)$', views.AdminBookEditView, name='admin_book_edit'),
    url(r'^book/detail/(?P<slug>[\w-]+)$', views.AdminBookDetailView, name='admin_book_detail'),

    ################################
    ################################
    # Request Book

    url(r'^request_book$', views.AdminListRequestBookView, name='admin_list_request_book'),
    url(r'^request_book/delete$', views.admin_delete_request_book, name='admin_delete_request_book'),
]
