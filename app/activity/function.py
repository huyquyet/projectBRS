import datetime

from app.activity.models import Activities, Activity, TypeActivity
from app.user.functions import check_user_activity, install_user_activity

__author__ = 'FRAMGIA\nguyen.huy.quyet'


def action(user_id, type_activity, object_id, data):
    int_type_activity = TypeActivity.objects.get(name=type_activity).pk
    # date_time = timezone.now()
    date_time = datetime.datetime.now()
    # date = date_time.date()
    # time = date_time.time()

    activities = Activities.objects.filter(_id=user_id)

    a = Activity()
    a.date_time = date_time
    a.type_activity = int_type_activity
    a.object_id = object_id
    a.data = data
    a.status = True

    activities.update_one(push__action=a)


def create_activity(user_id, type_activity, object_id, data):
    """ Install activity in database """
    check_user = check_user_activity(user_id)
    if check_user:
        action(user_id, type_activity, object_id, data)
    else:
        if install_user_activity(user_id):
            action(user_id, type_activity, object_id, data)
