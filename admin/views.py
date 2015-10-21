# Create your views here.
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import login
from django.contrib import auth
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView, UpdateView, DetailView, ListView, \
    CreateView

from admin.forms import BookCreateFormView

from book.models import Book

from category.models import Category

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

"""
Category
"""


class AdminCategoryIndex(ListView):
    model = Category
    template_name = 'admin/category/category_index.html'
    # context_object_name = ''
    paginate_by = 15


AdminCategoryIndexView = AdminCategoryIndex.as_view()


class AdminCategoryCreate(CreateView):
    model = Category
    template_name = 'admin/category/category_create.html'
    fields = ['name', 'slug']

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        return super(AdminCategoryCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('admin:admin_category_index')


AdminCategoryCreateView = AdminCategoryCreate.as_view()


class AdminCategoryDetail(DetailView):
    model = Category
    template_name = 'admin/category/category_detail.html'


AdminCategoryDetailView = AdminCategoryDetail.as_view()


class AdminCategoryEdit(UpdateView):
    model = Category
    template_name = 'admin/category/category_edit.html'
    fields = ['name', 'slug']

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        return super(AdminCategoryEdit, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('admin:admin_category_index')


AdminCategoryEditView = AdminCategoryEdit.as_view()

"""
Book
"""


class AdminBookIndex(ListView):
    model = Book
    template_name = 'admin/book/book_index.html'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        ctx = super(AdminBookIndex, self).get_context_data(**kwargs)
        for i in ctx['page_obj']:
            i.category = Category.objects.get(id=i.category.id)
        return ctx


AdminBookIndexView = AdminBookIndex.as_view()


class AdminBookCreate(CreateView):
    # model = Book
    template_name = 'admin/book/book_create.html'
    # fields = ['title', 'slug', 'category', 'cover', 'description', 'author', 'publish', 'page', 'price', 'date']
    form_class = BookCreateFormView

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        return super(AdminBookCreate, self).dispatch(request, *args, **kwargs)

    # def form_valid(self, form):
    #     form.save()
    #     return super(AdminBookCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('admin:admin_book_index')


AdminBookCreateView = AdminBookCreate.as_view()


class AdminBookEdit(UpdateView):
    model = Book
    template_name = 'admin/book/book_edit.html'
    form_class = BookCreateFormView

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        return super(AdminBookEdit, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('admin:admin_book_index')


AdminBookEditView = AdminBookEdit.as_view()


class AdminBookDetail(DetailView):
    model = Book
    template_name = 'admin/book/book_detail.html'

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        return super(AdminBookDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(AdminBookDetail, self).get_context_data(**kwargs)
        ctx['object'].point_rating = ctx['object'].get_rating_book()
        ctx['object'].rating = ctx['object'].rating_book.count()
        ctx['object'].review = ctx['object'].review_book.count()
        ctx['object'].slug_category = ctx['object'].category.slug

        return ctx


AdminBookDetailView = AdminBookDetail.as_view()
