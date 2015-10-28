# Create your views here.
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import login
from django.contrib import auth
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView, UpdateView, DetailView, ListView, CreateView
from django.db.models import Q

from admin.forms import BookCreateFormView
from book.models import Book
from category.models import Category
from sendbybook.models import ByBook

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
---------------------------------------------------------
 Book
---------------------------------------------------------

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

    def get(self, request, *args, **kwargs):
        search = self.request.GET.get('search', False)
        if search:
            search_1 = search.strip()
            self.queryset = Book.objects.filter(Q(title__icontains=search_1) | Q(category__name__icontains=search_1) | Q(author__icontains=search_1) | Q(publish__icontains=search_1))
        else:
            self.queryset = self.get_queryset()
        return super(AdminBookIndex, self).get(request, *args, **kwargs)


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


def admin_book_delete(request):
    request_book_id = request.POST.get('book_id', False)
    if request_book_id:
        obj = get_object_or_404(Book, pk=request_book_id)
        obj.delete()
        return HttpResponseRedirect(reverse_lazy('admin:admin_book_index'))
    else:
        return HttpResponseRedirect(reverse_lazy('admin:admin_book_index'))


"""
---------------------------------------------------------
Request Book
---------------------------------------------------------
"""


def count_book_request(count=None):
    if count is None:
        result = ByBook.objects.all().count()
    else:
        result = ByBook.objects.filter(status=count).count()
    return result


class AdminListRequestBook(ListView):
    model = ByBook
    template_name = 'admin/book/request/request_book_list.html'
    paginate_by = 15
    context_object_name = 'list_request_book'

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        return super(AdminListRequestBook, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(AdminListRequestBook, self).get_context_data(**kwargs)
        for i in ctx['list_request_book']:
            if i.status == 0:
                i.text_status = 'Waiting'
            elif i.status == 1:
                i.text_status = 'Successful'
            elif i.status == 2:
                i.text_status = 'Fail'
            else:
                i.status = 'Fail'
        ctx['total_send_book'] = count_book_request()
        ctx['successful_book'] = count_book_request(1)
        ctx['waiting_book'] = count_book_request(0)
        ctx['fail_book'] = count_book_request(2)
        return ctx


AdminListRequestBookView = AdminListRequestBook.as_view()


class AdminDetailRequestBook(DetailView):
    model = ByBook
    template_name = 'admin/book/request/request_book_detail.html'
    context_object_name = 'detail_request'

    @method_decorator(requirement_admin)
    def dispatch(self, request, *args, **kwargs):
        return super(AdminDetailRequestBook, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(AdminDetailRequestBook, self).get_context_data(**kwargs)
        ctx['detail_request'].full_name = ctx['detail_request'].user_profile.user.first_name + ' ' + ctx['detail_request'].user_profile.user.last_name
        if ctx['detail_request'].status == 0:
            ctx['detail_request'].text_status = 'Waiting'
        elif ctx['detail_request'].status == 1:
            ctx['detail_request'].text_status = 'Successful'
        elif ctx['detail_request'].status == 2:
            ctx['detail_request'].text_status = 'Fail'
        return ctx


AdminDetailRequestBookView = AdminDetailRequestBook.as_view()


def admin_delete_request_book(request):
    request_book_id = request.POST.get('request_book_id', False)
    if request_book_id:
        obj = get_object_or_404(ByBook, pk=request_book_id)
        obj.delete()
        return HttpResponseRedirect(reverse_lazy('admin:admin_list_request_book'))
    else:
        return HttpResponseRedirect(reverse_lazy('admin:admin_list_request_book'))


def admin_deny_request_book(request):
    request_book_id = request.POST.get('request_book_id', False)
    if request_book_id:
        obj = get_object_or_404(ByBook, pk=request_book_id)
        obj.status = 2
        obj.save()
        return HttpResponseRedirect(reverse_lazy('admin:admin_detail_request_book', kwargs={'pk': request_book_id}))
    else:
        return HttpResponseRedirect(reverse_lazy('admin:admin_list_request_book'))


def admin_accept_request_book(request):
    request_book_id = request.POST.get('request_book_id', False)
    if request_book_id:
        obj = get_object_or_404(ByBook, pk=request_book_id)
        obj.status = 1
        obj.save()
        return HttpResponseRedirect(reverse_lazy('admin:admin_detail_request_book', kwargs={'pk': request_book_id}))
    else:
        return HttpResponseRedirect(reverse_lazy('admin:admin_list_request_book'))
