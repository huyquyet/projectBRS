# Create your views here.
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin

from app.activity.function import create_activity
from app.base.views import BaseView
from app.book.models import Book, Rating, ReadReading, Favorite
from app.review.views import return_all_of_book
from app.user.models import Follow

"""
------------------------------------------------------------------------------

Book

------------------------------------------------------------------------------
"""


class BookIndex(BaseView, ListView):
    model = Book
    template_name = 'book/book_index.html'
    paginate_by = 12

    def dispatch(self, request, *args, **kwargs):
        time_now = timezone.now()

        try:
            user_id = self.request.user.pk
            follows = Follow.objects.filter(follower__user__id=user_id)
            for follow in follows:
                time = time_now - follow.date_level
                if time.seconds > 2 * 60 * 60:
                    if follow.level < 5:
                        follow.level += 1
                        follow.save()
        except:
            pass
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(BookIndex, self).get_context_data(**kwargs)
        for i in ctx['page_obj']:
            i.rate = i.get_rating_book()
            i.count_review = i.review_book.all().count()
        return ctx

    def get(self, request, *args, **kwargs):
        search = self.request.GET.get('search', False)
        if search:
            search_1 = search.strip()
            self.queryset = Book.objects.filter(
                Q(title__icontains=search_1) | Q(category__name__icontains=search_1) | Q(author__icontains=search) | Q(
                    publish__icontains=search_1)).order_by('-id')
        else:
            self.queryset = Book.objects.order_by('-id')
        return super(BookIndex, self).get(request, *args, **kwargs)


BookIndexView = BookIndex.as_view()


class BookDetail(BaseView, DetailView):
    model = Book
    template_name = 'book/book_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super(BookDetail, self).get_context_data(**kwargs)
        ctx['object'].point_rating = ctx['object'].get_rating_book()
        ctx['object'].rating = ctx['object'].rating_book.count()
        ctx['object'].review = ctx['object'].review_book.count()
        ctx['object'].slug_category = ctx['object'].category.slug
        ctx['object'].rate_book = return_rating_book(self.request.user, self.object)
        ctx['object'].number_rate_book = return_number_rating_book(self.request.user, self.object)
        ctx['object'].read_book = return_read_book(self.request.user, self.object)
        ctx['favorite'] = return_favorite_book(self.request.user, self.object)
        ctx['object'].review = return_number_review(self.object)
        ctx['review_all_book'] = return_all_of_book(self.object)
        # ctx['check_like_review'] = return_check_like_review(self.request.user, self.object)
        return ctx


BookDetailView = BookDetail.as_view()

"""
----------------------------------------------------------------------------

Rating

-----------------------------------------------------------------------------
"""


@login_required
def add_rating(request):
    rating = request.POST.get('rating', False)
    book_id = request.POST.get('book_id', False)
    user_id = request.POST.get('user_id', False)
    response_data = {}
    if book_id and rating:
        obj, create = Rating.objects.get_or_create(user_profile=request.user.user_profile,
                                                   book=Book.objects.get(pk=book_id))
        obj.rate = rating
        obj.save()
        try:
            """ Install activity in database """
            create_activity(request.user.pk, 'rating_book', book_id,
                            'Rating ' + rating + 'star in ' + Book.objects.get(pk=book_id).title)
        except:
            pass
        response_data['result'] = True
        response_data['number_point'] = Book.objects.get(id=book_id).get_rating_book()
        response_data['number_rating'] = Book.objects.get(id=book_id).rating_book.count()
        return JsonResponse(response_data)
    else:
        response_data['result'] = False
        return JsonResponse(response_data)


def return_rating_book(user, book):
    try:
        if Rating.objects.filter(user_profile=user.user_profile, book=book).exists():
            count_rating = return_number_rating_book(user, book)
            list_rating = [True if i <= count_rating else False for i in range(1, 6)]
            return list_rating
        else:
            list_rating = [False for i in range(1, 6)]
            return list_rating
    except:
        list_rating = [False for i in range(1, 6)]
        return list_rating


def return_number_rating_book(user, book):
    try:
        # if User.objects.filter(user_profile=user).exists():
        if Rating.objects.filter(user_profile=user.user_profile, book=book).exists():
            count_rating = Rating.objects.get(user_profile=user.user_profile, book=book).rate
            return count_rating
        else:
            return 0
    except:
        return


"""
-----------------------------------------------------------------------------------

Read book

-----------------------------------------------------------------------------------
"""


@login_required()
def want_read_book(request):
    book_id = request.POST.get('book_id', False)
    response_data = {}
    if book_id and request.user:
        obj, create = ReadReading.objects.get_or_create(user_profile=request.user.user_profile,
                                                        book=Book.objects.get(pk=book_id))
        obj.status = 1
        obj.save()

        """ Install activity in database """
        create_activity(request.user.pk, 'read_book', book_id, 'Reading book' + Book.objects.get(pk=book_id).title)

        response_data['result'] = 'Successful'
        return JsonResponse(response_data)
    else:
        response_data['result'] = 'Error'
        return JsonResponse(response_data)


"""
Return
0 : user not yet read or reading
1 : user reading
2 : user read
"""


def return_read_book(user, book):
    try:
        if ReadReading.objects.filter(user_profile=user.user_profile, book=book).exists():
            return ReadReading.objects.get(user_profile=user.user_profile, book=book).status
        else:
            return 0
    except:
        return 0


def read_finish(request):
    book_id = request.POST.get('book_id', False)
    response_data = {}
    if book_id and request.user:
        obj, create = ReadReading.objects.get_or_create(user_profile=request.user.user_profile,
                                                        book=Book.objects.get(pk=book_id))
        obj.status = 2
        obj.save()

        """ Install activity in database """
        create_activity(request.user.pk, 'finish_book', book_id,
                        'Finish read book' + Book.objects.get(pk=book_id).title)

        response_data['result'] = 'Successful'
        return JsonResponse(response_data)
    else:
        response_data['result'] = 'Error'
        return JsonResponse(response_data)


"""
-----------------------------------------------------------------------------------

Favorite book

-----------------------------------------------------------------------------------
"""


@login_required()
def favorite_book(request):
    book_id = request.POST.get('book_id', False)
    response_data = {}

    if book_id and request.user:
        obj, create = Favorite.objects.get_or_create(user_profile=request.user.user_profile,
                                                     book=Book.objects.get(pk=book_id))
        obj.save()
        try:
            """ Install activity in database """
            create_activity(request.user.pk, 'favorite', book_id,
                            'Favorite book ' + Book.objects.get(pk=book_id).title)
        except:
            pass
        response_data['result'] = True
        return JsonResponse(response_data)
    else:
        response_data['result'] = False
        return JsonResponse(response_data)


def return_favorite_book(user, book):
    try:
        if Favorite.objects.filter(user_profile=user.user_profile, book=book).exists():
            return True
        else:
            return False
    except:
        return False


@login_required()
def un_favorite_book(request):
    book_id = request.POST.get('book_id', False)
    response_data = {}

    if book_id and request.user:
        obj = Favorite.objects.get(user_profile=request.user.user_profile,
                                   book=Book.objects.get(pk=book_id))
        obj.delete()
        response_data['result'] = True
        return JsonResponse(response_data)
    else:
        response_data['result'] = False
        return JsonResponse(response_data)


"""
-----------------------------------------------------------------------------------

Review book

-----------------------------------------------------------------------------------
"""


def return_number_review(book):
    return book.review_book.all().count()


"""
-----------------------------------------------------------------------------------

Manager book

-----------------------------------------------------------------------------------
"""

"""
status = 1 reading
status = 2 read
"""


def return_list_book_read(user, status=None, count=None, search=None):
    list_read = ReadReading.objects.filter(user_profile=user.user_profile, status=status).order_by('-date').values_list(
        'book', flat=True)
    if search is None:
        list_book = Book.objects.filter(id__in=list_read)[0:count]
    else:
        list_book = Book.objects.filter(id__in=list_read, title__contains=search)[0:count]
    for i in list_book:
        i.rate = i.get_rating_book()
        i.count_review = i.review_book.all().count()
    return list_book


def return_list_book_favorite(user, count=None, search=None):
    list_favorite = Favorite.objects.filter(user_profile=user.user_profile).order_by('-date').values_list('book',
                                                                                                          flat=True)
    if search is None:
        list_book = Book.objects.filter(id__in=list_favorite)[0:count]
    else:
        list_book = Book.objects.filter(id__in=list_favorite, title__contains=search)[0:count]
    for i in list_book:
        i.rate = i.get_rating_book()
        i.count_review = i.review_book.all().count()
    return list_book


class BookManager(BaseView, SingleObjectMixin, ListView):
    model = User
    template_name = 'book/book_manager.html'
    context_object_name = 'UserName'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.object = User.objects.get(username=self.kwargs['username'])
        return self.object

    def get_context_data(self, **kwargs):
        search = self.request.GET.get('search', None)
        count = 6
        ctx = super(BookManager, self).get_context_data(**kwargs)
        ctx['list_book_read'] = return_list_book_read(self.object, 2, count, search)
        ctx['list_book_reading'] = return_list_book_read(self.object, 1, count, search)
        ctx['list_book_favorite'] = return_list_book_favorite(self.object, count, search)
        return ctx


BookManagerView = BookManager.as_view()


class BookManagerRead(BaseView, SingleObjectMixin, ListView):
    model = User
    template_name = 'book/book_manager_read.html'
    paginate_by = 8
    context_object_name = 'UserName'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.object = User.objects.get(username=self.kwargs['username'])
        return self.object

    def get_queryset(self):
        count = None
        status = 2
        search = self.request.GET.get('search', None)
        books = return_list_book_read(self.object, status, count, search)
        return books


BookManagerReadView = BookManagerRead.as_view()


class BookManagerReading(BaseView, SingleObjectMixin, ListView):
    model = User
    template_name = 'book/book_manager_reading.html'
    paginate_by = 8
    context_object_name = 'UserName'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.object = User.objects.get(username=self.kwargs['username'])
        return self.object

    def get_queryset(self):
        count = None
        status = 1
        search = self.request.GET.get('search', None)
        books = return_list_book_read(self.object, status, count, search)
        return books


BookManagerReadingView = BookManagerReading.as_view()


class BookManagerFavorite(BaseView, SingleObjectMixin, ListView):
    model = User
    template_name = 'book/book_manager_favorite.html'
    paginate_by = 8
    context_object_name = 'UserName'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.object = User.objects.get(username=self.kwargs['username'])
        return self.object

    def get_queryset(self):
        count = None
        search = self.request.GET.get('search', None)
        books = return_list_book_favorite(self.object, count, search)
        return books


BookManagerFavoriteView = BookManagerFavorite.as_view()
