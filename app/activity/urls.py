from django.conf.urls import url
from app.activity.views  import  user

__author__ = 'FRAMGIA\nguyen.huy.quyet'
urlpatterns = [

    ################################
    # Profile

    url(r'^$', user.ActivityUserIndexView, name='activity_user_index'),
    url(r'^activity$', user.return_list_activity_user, name='return_list_activity_user'),

]
