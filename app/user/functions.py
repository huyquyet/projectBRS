from app.activity.models import Activities

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
