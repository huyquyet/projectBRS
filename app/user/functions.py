from django.utils import timezone

from app.activity.models import Activities
from app.user.models import Follow

__author__ = 'FRAMGIA\nguyen.huy.quyet'


def check_user_activity(pk):
    user = Activities.objects(_id=pk)
    if user:
        return True
    else:
        return False


def install_user_activity(pk):
    try:
        user = Activities(_id=pk)
        user.save()
        return True
    except:
        return False


def change_follow_level(follower, followee):
    """
    Change level follow
    :param follower:
    :param followee:
    :return: update level and date_level follow
    """
    follow = Follow.objects.get(follower=follower, followee=followee)
    print(follow.level)
    if follow.level > 1:
        follow.level -= 1
    follow.date_level = timezone.now()
    follow.save()
