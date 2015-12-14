from datetime import datetime

from mongoengine import DoesNotExist

from app.activity.models import Activities, Activity, TypeActivity
from app.user.functions import check_user_activity, install_user_activity
from app.user.models import UserProfile, Follow

__author__ = 'FRAMGIA\nguyen.huy.quyet'


def action(user_id, type_activity, object_id, data):
    int_type_activity = TypeActivity.objects.get(name=type_activity).pk
    date_time = datetime.now()

    activities = Activities.objects.filter(_id=user_id)

    a = Activity()
    a._id = user_id
    a.date_time = date_time
    # a.date = date_time.date()
    # a.time = date_time.time()
    a.type_activity = int_type_activity
    a.object_id = object_id
    a.data = data
    a.status = True

    print(a.date_time)

    activities.update_one(push__action=a)


def create_activity(user_id, type_activity, object_id, data):
    """ Install activity in database """
    check_user = check_user_activity(user_id)
    if check_user:
        action(user_id, type_activity, object_id, data)
    else:
        if install_user_activity(user_id):
            action(user_id, type_activity, object_id, data)


def return_list_activity_user(user_id):
    profile_id = UserProfile.objects.get(user__id=user_id).pk
    list_id_profile = Follow.objects.filter(follower=profile_id, level__lt=5).values_list('followee', flat=True)
    list_id_user = [UserProfile.objects.get(pk=i).user.pk for i in list_id_profile]
    activities = []
    minutes = 5  # Khoảng thời gian cho mỗi lần load
    minutes_delta = minutes
    time_now = datetime.now()
    # time_delta = time_now - timedelta(minutes=minutes)
    count_action = [0] * len(list_id_user)
    array_check = [True] * len(list_id_user)
    for i in range(len(list_id_user)):
        try:
            lens_action = len(Activities.objects.get(_id=list_id_user[i]).action)
            # , action__date_time__gt=time_delta,action__date_time__lt=time_now
            count_action[i] = lens_action
            array_check[i] = False
        except DoesNotExist:
            array_check[i] = True
            continue

    while len(activities) <= 10:
        for i in range(len(list_id_user)):
            if count_action[i] is not None:
                while count_action[i] > 0:
                    activity = Activities.objects.get(_id=list_id_user[i]).action[count_action[i] - 1]
                    if (time_now - activity.date_time).total_seconds() < minutes_delta * 60 and (
                                time_now - activity.date_time).total_seconds() > (minutes_delta - 30) * 60:
                        activities.append(activity)
                        count_action[i] -= 1
                        if count_action[i] > 0:
                            array_check[i] = False
                        else:
                            array_check[i] = True
                    else:
                        break
            else:
                continue
        total_empty = True
        for is_empty in array_check:
            if is_empty is False:
                total_empty = False
        if total_empty:
            break
        minutes_delta += minutes
    activities.sort(key=lambda a: a.date_time, reverse=True)
    return activities
