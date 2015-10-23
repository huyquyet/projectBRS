# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView

from book.models import Book, Rating, ReadReading, Favorite

"""
------------------------------------------------------------------------------

Book

------------------------------------------------------------------------------
"""


class BookIndex(ListView):
    model = Book
    template_name = 'book/book_index.html'
    paginate_by = 12


BookIndexView = BookIndex.as_view();


class BookDetail(DetailView):
    model = Book
    template_name = 'book/book_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super(BookDetail, self).get_context_data(**kwargs)
        ctx['object'].point_rating = ctx['object'].get_rating_book()
        ctx['object'].rating = ctx['object'].rating_book.count()
        ctx['object'].review = ctx['object'].review_book.count()
        ctx['object'].slug_category = ctx['object'].category.slug
        ctx['object'].rate_book = return_rating_book(self.request.user, self.object)
        ctx['object'].read_book = return_read_book(self.request.user, self.object)
        ctx['favorite'] = return_favorite_book(self.request.user, self.object)
        return ctx

        # def post(self, request, *args, **kwargs):
        #     return add_rating(request)


BookDetailView = BookDetail.as_view()

"""
----------------------------------------------------------------------------

Rating

-----------------------------------------------------------------------------
"""


@login_required
def add_rating(request):
    point = request.POST.get('point_rating', False)
    book_id = request.POST.get('book_id', False)

    if book_id and point:
        obj, create = Rating.objects.get_or_create(user_profile=request.user.user_profile, book=Book.objects.get(pk=book_id))
        obj.rate = point
        obj.save()
        slug_book = Book.objects.get(pk=book_id).slug
        return HttpResponseRedirect(reverse("book:book_detail", kwargs={'slug': slug_book}))
    elif point:
        return HttpResponseRedirect(reverse("book:book_index"))
    elif book_id:
        slug_book = Book.objects.get(pk=book_id).slug
        return HttpResponseRedirect(reverse("book:book_detail", kwargs={'slug': slug_book}))
    else:
        return HttpResponseRedirect(reverse("book:book_index"))


def return_rating_book(user, book):
    try:
        # if User.objects.filter(user_profile=user).exists():
        if Rating.objects.filter(user_profile=user.user_profile, book=book).exists():
            return Rating.objects.get(user_profile=user.user_profile, book=book).rate
        else:
            return 0
    except:
        return 0


"""
-----------------------------------------------------------------------------------

Read book

-----------------------------------------------------------------------------------
"""


@login_required()
def want_read_book(request):
    book_id = request.POST.get('book_id', False)

    if book_id and request.user:
        obj, create = ReadReading.objects.get_or_create(user_profile=request.user.user_profile, book=Book.objects.get(pk=book_id))
        obj.status = 1
        obj.save()
        slug_book = Book.objects.get(pk=book_id).slug
        return HttpResponseRedirect(reverse("book:book_detail", kwargs={'slug': slug_book}))
    elif request.user:
        return HttpResponseRedirect(reverse("book:book_index"))
    elif book_id:
        slug_book = Book.objects.get(pk=book_id).slug
        return HttpResponseRedirect(reverse("book:book_detail", kwargs={'slug': slug_book}))
    else:
        return HttpResponseRedirect(reverse("book:book_index"))


"""
Return
0 : user not yet read or reading
1 : user reading
2 : user read
"""


def return_read_book(user, book):
    try:
        # if User.objects.filter(user_profile=user).exists():
        if ReadReading.objects.filter(user_profile=user.user_profile, book=book).exists():
            return ReadReading.objects.get(user_profile=user.user_profile, book=book).status
        else:
            return 0
    except:
        return 0


"""
-----------------------------------------------------------------------------------

Favorite book

-----------------------------------------------------------------------------------
"""


@login_required()
def favorite_book(request):
    book_id = request.POST.get('book_id', False)

    if book_id and request.user:
        obj, create = Favorite.objects.get_or_create(user_profile=request.user.user_profile, book=Book.objects.get(pk=book_id))
        obj.save()
        slug_book = Book.objects.get(pk=book_id).slug
        return HttpResponseRedirect(reverse("book:book_detail", kwargs={'slug': slug_book}))
    elif request.user:
        return HttpResponseRedirect(reverse("book:book_index"))
    elif book_id:
        slug_book = Book.objects.get(pk=book_id).slug
        return HttpResponseRedirect(reverse("book:book_detail", kwargs={'slug': slug_book}))
    else:
        return HttpResponseRedirect(reverse("book:book_index"))


def return_favorite_book(user, book):
    try:
        # if User.objects.filter(user_profile=user).exists():
        if Favorite.objects.filter(user_profile=user.user_profile, book=book).exists():
            return True
        else:
            return False
    except:
        return False
