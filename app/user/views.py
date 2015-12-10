# Create your views here.
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView, UpdateView, ListView
from django.views.generic.detail import SingleObjectMixin

from app.activity.function import create_activity
from app.base.views import BaseView
from app.book.views import return_list_book_read, return_list_book_favorite
from app.review.functions import return_list_review_of_user
from app.user.functions import change_follow_level
from app.user.models import UserProfile, Follow


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
        link = self.request.POST.get('next', '')
        if link:
            return link
        else:
            return reverse('user:user_index')


UserLoginView = UserLogin.as_view()


def UserLogoutView(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('user:user_index'))


# UserLogoutView = UserLogout.as_view()


class UserRegister(FormView):
    form_class = UserCreationForm
    template_name = 'user/user_register.html'

    def form_valid(self, form):
        form.instance.is_staff = False

        user = form.save()
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        # user_profile.save()
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


class UserChangePass(UpdateView):
    model = User
    template_name = 'user/user_change_pass.html'
    form_class = PasswordChangeForm
    # fields = ['first_name', 'last_name', 'email']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != request.user:
            raise PermissionDenied
        return super(UserChangePass, self).dispatch(request, *args, **kwargs)

    # def form_valid(self, form):
    def get_object(self, queryset=None):
        self.object = User.objects.get(username=self.kwargs['username'])
        return self.object

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


UserChangePassView = UserChangePass.as_view()

"""
--------------------------------------------------------------------------------

User Follow

--------------------------------------------------------------------------------
"""


def return_list_following_of_user(user):
    try:
        following = Follow.objects.filter(follower=user.user_profile).values_list('followee', flat=True)
        list_user_following = User.objects.filter(user_profile__id__in=following)
        for i in list_user_following:
            i.count_favorite = return_list_book_favorite(i).count()
            i.count_reading_book = return_list_book_read(i, 1).count()
            i.check_follow = False
        return list_user_following
    except:
        return []


def return_list_followers_of_user(user):
    try:
        followers = Follow.objects.filter(followee=user.user_profile).values_list('follower', flat=True)
        list_user_followers = User.objects.filter(user_profile__id__in=followers)
        list_following = return_list_following_of_user(user)
        for i in list_user_followers:
            i.count_favorite = return_list_book_favorite(i).count()
            i.count_reading_book = return_list_book_read(i, 1).count()
            if i in list_following:
                i.check_follow = False
            else:
                i.check_follow = True
        return list_user_followers
    except:
        return []


class UserManageFollow(BaseView, SingleObjectMixin, ListView):
    model = User
    template_name = 'user/follow/user_follow.html'
    paginate_by = 12

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.object = User.objects.get(username=self.kwargs['username'])
        return self.object

    def get_context_data(self, **kwargs):
        ctx = super(UserManageFollow, self).get_context_data(**kwargs)
        ctx['list_follow'] = return_list_following_of_user(self.object)
        ctx['check'] = 'following'
        for i in ctx['list_follow']:
            i.count_favorite = return_list_book_favorite(i).count()
            i.count_reading_book = return_list_book_read(i, 1).count()
            i.check_follow = False
        return ctx


UserManageFollowView = UserManageFollow.as_view()


class UserManageFollowers(BaseView, SingleObjectMixin, ListView):
    model = User
    template_name = 'user/follow/user_follow.html'
    paginate_by = 12

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.object = User.objects.get(username=self.kwargs['username'])
        return self.object

    def get_context_data(self, **kwargs):
        ctx = super(UserManageFollowers, self).get_context_data(**kwargs)

        """---------return list user following---------"""
        ctx['list_follow'] = return_list_followers_of_user(self.object)
        ctx['check'] = 'followers'
        return ctx


UserManageFollowersView = UserManageFollowers.as_view()


class UserHomePage(BaseView, SingleObjectMixin, ListView):
    model = User
    template_name = 'user/follow/home_page.html'
    context_object_name = 'UserName'

    # def dispatch(self, request, *args, **kwargs):
    #
    #     return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.object = User.objects.get(username=self.kwargs['username'])
        if self.object in return_list_following_of_user(self.request.user):
            """ Change the follow level """
            change_follow_level(follower=self.request.user.user_profile, followee=self.object.user_profile)
        return self.object

    def get_context_data(self, **kwargs):
        ctx = super(UserHomePage, self).get_context_data(**kwargs)
        if self.object in return_list_following_of_user(self.request.user) or self.object == self.request.user:
            search = self.request.GET.get('search', None)
            count = 6
            ctx['check'] = True
            ctx['count_favorite'] = return_list_book_favorite(self.object).count()
            ctx['count_reading_book'] = return_list_book_read(self.object, 1).count()
            ctx['list_book_read'] = return_list_book_read(self.object, 2, count, search)
            ctx['list_book_reading'] = return_list_book_read(self.object, 1, count, search)
            ctx['list_book_favorite'] = return_list_book_favorite(self.object, count, search)
            ctx['list_user_following'] = return_list_following_of_user(self.object)
            ctx['list_user_followers'] = return_list_followers_of_user(self.object)
            ctx['list_user_review'] = return_list_review_of_user(self.object)
            if self.object == self.request.user:
                ctx['user_profile'] = True
        else:
            ctx['check'] = False
            ctx['count_favorite'] = return_list_book_favorite(self.object).count()
            ctx['count_reading_book'] = return_list_book_read(self.object, 1).count()
        return ctx


UserHomePageView = UserHomePage.as_view()


@login_required()
def user_follower(request):
    followers_user_id = request.POST.get('followers_user_id', False)
    user = request.user
    if followers_user_id and user is not None:
        obj, create = Follow.objects.get_or_create(follower=UserProfile.objects.get(user=request.user),
                                                   followee=UserProfile.objects.get(user__id=followers_user_id))
        obj.level = 1
        obj.save()

        """ Install activity in database """
        first_name = User.objects.get(pk=followers_user_id).first_name
        last_name = User.objects.get(pk=followers_user_id).last_name

        create_activity(request.user.pk, 'read_book', followers_user_id, 'Unfollow you' + first_name + last_name)

        return HttpResponseRedirect(
            reverse_lazy('user:user_home_page', kwargs={'username': User.objects.get(pk=followers_user_id).username}))
    else:
        return HttpResponseRedirect(
            reverse_lazy('user:user_manager_followers', kwargs={'username': request.user}))


@login_required()
def user_un_follow(request):
    user_follow_id = request.POST.get('user_id', False)
    user = request.user
    location = request.POST.get('location', '')
    if user_follow_id and user is not None:
        obj = get_object_or_404(Follow, follower=UserProfile.objects.get(user=request.user),
                                followee=UserProfile.objects.get(user=User.objects.get(pk=user_follow_id)))
        obj.delete()

        """ Install activity in database """
        first_name = User.objects.get(pk=user_follow_id).first_name
        last_name = User.objects.get(pk=user_follow_id).last_name

        create_activity(request.user.pk, 'read_book', user_follow_id, 'Unfollow you' + first_name + last_name)

        if location == 'user_follow':
            return HttpResponseRedirect(reverse_lazy('user:user_manager_follow', kwargs={'username': user.username}))
        else:
            return HttpResponseRedirect(
                reverse_lazy('user:user_home_page', kwargs={'username': User.objects.get(pk=user_follow_id).username}))
    else:
        if location == 'user_follow':
            return HttpResponseRedirect(reverse_lazy('user:user_manager_follow', kwargs={'username': user.username}))
        else:
            return HttpResponseRedirect(
                reverse_lazy('user:user_home_page', kwargs={'username': request.user}))
