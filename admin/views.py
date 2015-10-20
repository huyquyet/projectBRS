# Create your views here.
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import login
from django.contrib import auth
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView, UpdateView, DetailView

requirement_admin = user_passes_test(lambda u: u.is_staff, login_url='admin:admin_login')


class AdminIndexView(TemplateView):
    template_name = 'admin/layout/base_admin.html'

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


AdminIndexView = AdminIndexView.as_view()


class AdminLoginView(FormView):
    form_class = AdminAuthenticationForm
    template_name = 'admin/admin_login.html'

    def get_success_url(self):
        link = self.request.POST.get('next', False)
        if link:
            return link
        else:
            return reverse('admin:admin_index')

    def form_valid(self, form):
        user_form = form.get_user()
        login(self.request, user_form)
        return super().form_valid(form)


AdminLoginView = AdminLoginView.as_view()


@requirement_admin
def logout_admin(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('admin:admin_index'))


class AdminProfileView(DetailView):
    model = User
    template_name = 'admin/admin_detail_profile.html'
    context_object_name = ''

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


AdminProfileView = AdminProfileView.as_view()


class AdminEditProfileView(UpdateView):
    model = User
    template_name = 'admin/admin_edit_profile.html'
    # context_object_name = ''
    fields = ['first_name', 'last_name', 'email']

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('admin:admin_detail_profile', kwargs={'pk': self.request.user.id})


AdminEditProfileView = AdminEditProfileView.as_view()
