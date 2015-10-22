# Create your views here.
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView, View, UpdateView

from user.models import UserProfile


class UserIndex(TemplateView):
    # model = Book
    # template_name = 'user/user_index.html'
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('book:book_index'))


UserIndexView = UserIndex.as_view()


class UserLogin(FormView):
    form_class = AuthenticationForm
    template_name = 'user/user_login.html'

    def form_valid(self, form):
        user_form = form.get_user()
        login(self.request, user_form)
        return super(UserLogin, self).form_valid(form)

    def get_success_url(self):
        link = self.request.POST.get('link', '')
        if link:
            return link
        else:
            return reverse('user:user_index')


UserLoginView = UserLogin.as_view()


class UserLogout(View):
    # @login_required()
    def post(self, request, *args, **kwargs):
        auth.logout(request)
        return HttpResponseRedirect(reverse('user:user_index'))


UserLogoutView = UserLogout.as_view()


class UserRegister(FormView):
    form_class = UserCreationForm
    template_name = 'user/user_register.html'

    def form_valid(self, form):
        form.instance.is_staff = False
        form.save()
        return super(UserRegister, self).form_valid(form)

    def get_success_url(self):
        return reverse('user:user_login')


UserRegisterView = UserRegister.as_view()


class UserEditProfile(UpdateView):
    model = User
    template_name = 'user/user_edit_profile.html'
    fields = ['first_name', 'last_name', 'email']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != request.user:
            raise PermissionDenied
        return super(UserEditProfile, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.object = User.objects.get(username=self.kwargs['username'])
        return self.object

    def get_success_url(self):
        return reverse('user:user_index')


UserEditProfileView = UserEditProfile.as_view()


class UserChangPass(UpdateView):
    model = UserProfile
    template_name = 'user/user_change_pass.html'
    form_class = PasswordChangeForm
    # fields = ['first_name', 'last_name', 'email']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != request.user:
            raise PermissionDenied
        return super(UserChangPass, self).dispatch(request, *args, **kwargs)

    # def form_valid(self, form):

    def get_success_url(self):
        return reverse('user:user_login')

        # if request.method == 'POST':
        #     form = PasswordChangeForm(user=request.user, data=request.POST)
        #     if form.is_valid():
        #         form.save()
        #         return HttpResponseRedirect(reverse('fels:index'))
        # else:
        #     form = PasswordChangeForm(user=request.user)
        # return render(request, 'user/change_pass.html', {'form': form})


UserChangPassView = UserChangPass.as_view()
