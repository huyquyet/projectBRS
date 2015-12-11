from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from app.activity.function import return_list_activity_user
from app.activity.models import Activities, TypeActivity
from app.base.views import BaseView

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
