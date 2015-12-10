from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

from django.views.generic import ListView
from mongoengine import DoesNotExist

from app.activity.models import Activities, TypeActivity
from app.base.views import BaseView
from app.user.models import UserProfile, Follow

__author__ = 'FRAMGIA\nguyen.huy.quyet'


class ActivityUserIndex(BaseView, ListView):
    model = Activities
    template_name = 'activity/user/index.html'
    # context_object_name = 'list_activity'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.queryset = Activities.objects.get(_id=self.request.user.pk)
        return self.queryset

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['actions'] = []
        activities = return_list_activity_user(self.request.user.pk)
        for action in activities:
            action.id = action._id
            action.type_activity = TypeActivity.objects.get(pk=action.type_activity).name
            ctx['actions'].append(action)
        return ctx


ActivityUserIndexView = ActivityUserIndex.as_view()


def return_list_activity_user(user_id):
    profile_id = UserProfile.objects.get(user__id=user_id).pk
    list_id_profile = Follow.objects.filter(follower=profile_id, level__lt=5).values_list('followee', flat=True)
    list_id_user = [UserProfile.objects.get(pk=i).user.pk for i in list_id_profile]
    activities = []
    for i in list_id_user:
        try:
            activities += Activities.objects.get(_id=i).action
        except DoesNotExist:
            pass
    activities.sort(key=lambda a: a.date_time, reverse=True)
    return activities
