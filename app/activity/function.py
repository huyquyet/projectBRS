from datetime import datetime

from django.http import JsonResponse
from django.template.loader import render_to_string
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


def return_array_number_action_of_activity(list_id_user):
    count_action = [0] * len(list_id_user)
    for i in range(len(list_id_user)):
        try:
            """ return num action of user """
            lens_action = len(Activities.objects.get(_id=list_id_user[i]).action)
            count_action[i] = lens_action
        except DoesNotExist:
            continue
    return count_action


def return_list_activity_user(user_id, time):
    profile_id = UserProfile.objects.get(user__id=user_id).pk
    list_id_profile = Follow.objects.filter(follower=profile_id, level__lt=5).values_list('followee', flat=True)
    list_id_user = [UserProfile.objects.get(pk=i).user.pk for i in list_id_profile]
    activities = []

    """  Khoảng thời gian cho mỗi lần load  """
    minutes = 10
    minutes_delta = minutes + time
    time_now = datetime.now()

    """  Đếm số action cho mỗi user  """
    # count_action = [0] * len(list_id_user)

    """  Array check hết end action   """
    array_check = [False] * len(list_id_user)

    count_action = return_array_number_action_of_activity(list_id_user)

    """ Lấy data khi nào đủ 5 bản ghi thì thôi """
    while len(activities) <= 5:
        for i in range(len(list_id_user)):
            if count_action[i] is not None:

                """ Dừng lại khi số phần tử trong mảng = 0  """
                while count_action[i] > 0:

                    """ Lấy về 1 object action  """
                    activity = Activities.objects.get(_id=list_id_user[i]).action[count_action[i] - 1]

                    """ Kiểm tra xem object lấy về có nằm trong khoảng thời gian cần lấy hay ko """
                    if (time_now - activity.date_time).total_seconds() < minutes_delta * 60 and (
                                time_now - activity.date_time).total_seconds() > (minutes_delta - 30) * 60:
                        activity.time = minutes_delta
                        activity.action = count_action[i]
                        activities.append(activity)
                        count_action[i] -= 1

                        """ Nếu trong mảng vẫn còn phần tử """
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
    print(minutes_delta)
    activities.sort(key=lambda a: a.date_time, reverse=True)
    activities_r = []
    for i in range(len(activities)):
        activities[i].id = activities[i]._id
        activities[i].type_activity = TypeActivity.objects.get(pk=activities[i].type_activity).name
        print(activities[i].id)
        activities_r.append(render_to_string('activity/user/action.html', {'actions', activities[i]}))
    print(activities_r)

    response_data = {
        'activities': activities_r,
        'count_action': count_action
    }
    return JsonResponse(response_data)
