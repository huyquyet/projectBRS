from django.conf.urls import url
from app.activity.views  import  user

__author__ = 'FRAMGIA\nguyen.huy.quyet'
urlpatterns = [

    ################################
    # Profile

    url(r'^$', user.ActivityUserIndexView, name='activity_user_index'),
]
