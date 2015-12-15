from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from app.activity.function import return_array_number_action_of_activity
from app.activity.models import Activities, TypeActivity
from app.base.views import BaseView
from app.user.models import UserProfile, Follow

__author__ = 'FRAMGIA\nguyen.huy.quyet'


class ActivityUserIndex(BaseView, TemplateView):
    model = Activities
    template_name = 'activity/user/index.html'
    # context_object_name = 'list_activity'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # def get_queryset(self):
    #     self.queryset = Activities.objects.get(_id=self.request.user.pk)
    #     return self.queryset

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # ctx['actions'] = []
        # activities, list_id_user, count_action = return_list_activity_user(self.request.user.pk, 0)
        # for action in activities:
        #     action.id = action._id
        #     action.type_activity = TypeActivity.objects.get(pk=action.type_activity).name
        #     ctx['actions'].append(action)
        # self.request.session['count_action'] = count_action
        return ctx


ActivityUserIndexView = ActivityUserIndex.as_view()


def return_list_activity_user(request):
    profile_id = UserProfile.objects.get(user__id=request.user.id).pk
    list_id_profile = Follow.objects.filter(follower=profile_id, level__lt=5).values_list('followee', flat=True)
    list_id_user = [UserProfile.objects.get(pk=i).user.pk for i in list_id_profile]
    activities = []

    """  Khoảng thời gian cho mỗi lần load  """
    minutes = 1
    minutes_delta = minutes
    time_now = datetime.now()

    """  Đếm số action cho mỗi user  """
    # count_action = [0] * len(list_id_user)

    """  Array check hết end action   """
    array_check = [False] * len(list_id_user)

    count_action = return_array_number_action_of_activity(list_id_user)

    """ Lấy data khi nào đủ 5 bản ghi thì thôi """
    time_now_1 = datetime.now()
    while len(activities) <= 20:
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
    time_now_2 = datetime.now()
    print(time_now_2 - time_now_1)
    activities.sort(key=lambda a: a.date_time, reverse=True)
    activities_r = []
    for i in range(len(activities)):
        activities[i].id = activities[i]._id
        activities[i].type_activity = TypeActivity.objects.get(pk=activities[i].type_activity).name
        # activitie.date_time = activitie.date_time
        activities_r.append(render_to_string('activity/user/action.html', {'action': activities[i], 'i': i}))
        # a = render_to_string('activity/user/action.html', {'action': activities[i]})
        # activities_r.append(activity)

    response_data = {
        'activities': activities_r,
        'count_action': count_action
    }
    # response_data['activities'] = activities_r
    # response_data['count_action'] = count_action
    # return activities, list_id_user, count_action
    return JsonResponse(response_data)
