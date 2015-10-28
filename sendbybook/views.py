# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView

from django.views.generic.detail import SingleObjectMixin

from base.views import BaseView
from sendbybook.forms import SendNewBookFormView
from sendbybook.models import ByBook
from user.models import UserProfile


class SendNewBook(BaseView, CreateView):
    form_class = SendNewBookFormView
    template_name = 'book/sendbook/send_new_book.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SendNewBook, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user_profile = UserProfile.objects.get(user=self.request.user)
        form.instance.status = False
        form.save()
        return super(SendNewBook, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('send:send_book_manager')


SendNewBookView = SendNewBook.as_view()


class SendBookManager(BaseView, SingleObjectMixin, ListView):
    model = ByBook
    template_name = 'book/sendbook/send_book_manager.html'
    context_object_name = 'list_send_book'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SendBookManager, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(SendBookManager, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.object = ByBook.objects.filter(user_profile=self.request.user.user_profile)
        return self.object

    def get_context_data(self, **kwargs):
        ctx = super(SendBookManager, self).get_context_data(**kwargs)
        for i in ctx['list_send_book']:
            if i.status == 0:
                i.text_status = 'Waiting'
            elif i.status == 1:
                i.text_status = 'Successful'
            elif i.status == 2:
                i.text_status = 'Fail'
            else:
                i.status = 'Fail'
        ctx['total_send_book'] = count_book_of_user(self.request.user)
        ctx['successful_book'] = count_book_of_user(self.request.user, 1)
        ctx['waiting_book'] = count_book_of_user(self.request.user, 0)
        ctx['fail_book'] = count_book_of_user(self.request.user, 2)
        return ctx


SendBookManagerView = SendBookManager.as_view()


class SendBookDetail(DetailView):
    model = ByBook
    template_name = ''


SendBookDetailView = SendBookDetail.as_view()


def delete_book(request):
    send_book_id = request.POST.get('send_book_id', False)
    if send_book_id:
        obj = get_object_or_404(ByBook, pk=send_book_id)
        if request.user == UserProfile.objects.get(user=obj.user):
            obj.delete()
            return HttpResponseRedirect(reverse_lazy('send:send_book_manager'))
        else:
            return HttpResponseRedirect(reverse_lazy('send:send_book_manager'))
    else:
        return HttpResponseRedirect(reverse_lazy('send:send_book_manager'))


def count_book_of_user(user, count=None):
    if count is None:
        result = ByBook.objects.filter(user_profile=user.user_profile).count()
    else:
        result = ByBook.objects.filter(user_profile=user.user_profile, status=count).count()
    return result
