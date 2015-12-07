from django.conf.urls import url

from app.user import views

__author__ = 'FRAMGIA\nguyen.huy.quyet'

urlpatterns = [
    #######################################
    #######################################
    # User

    url(r'^$', views.UserIndexView, name='user_index'),
    url(r'^login$', views.UserLoginView, name='user_login'),
    url(r'^logout$', views.UserLogoutView, name='user_logout'),
    url(r'^register$', views.UserRegisterView, name='user_register'),
    url(r'^(?P<username>[\w-]+)/edit$', views.UserEditProfileView, name='user_edit_profile'),
    url(r'^(?P<username>[\w-]+)/change_pass$', views.UserChangePassView, name='user_change_pass'),

    url(r'^home/(?P<username>[\w-]+)/$', views.UserHomePageView, name='user_home_page'),
    url(r'^home/follow$', views.user_follower, name='user_follow'),
    url(r'^home/un_follow$', views.user_un_follow, name='user_un_follow'),
    url(r'^home/(?P<username>[\w-]+)/book$', views.UserHomePageView, name='user_f_book'),

    url(r'^(?P<username>[\w-]+)/following$', views.UserManageFollowView, name='user_manager_follow'),
    url(r'^(?P<username>[\w-]+)/followers', views.UserManageFollowersView, name='user_manager_followers'),



    url(r'^test_ajax/', views.test_ajax, name='test_ajax'),
    url(r'^test_ajax_result/', views.test_ajax_result, name='test_ajax_result'),
]
