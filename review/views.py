# Create your views here.
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect

from book.models import Book
from review.models import Review, LikeReview


def review_create(request):
    book_id = request.POST.get('book_id', False)
    content_review = request.POST.get('content_review', False)

    if book_id and request.user:
        obj, create = Review.objects.get_or_create(user_profile=request.user.user_profile, book=Book.objects.get(pk=book_id))
        obj.content = content_review
        obj.save()
        slug_book = Book.objects.get(pk=book_id).slug
        return HttpResponseRedirect(reverse_lazy("book:book_detail", kwargs={'slug': slug_book}))
    elif request.user:
        return HttpResponseRedirect(reverse_lazy("book:book_index"))
    elif book_id:
        slug_book = Book.objects.get(pk=book_id).slug
        return HttpResponseRedirect(reverse_lazy("book:book_detail", kwargs={'slug': slug_book}))
    else:
        return HttpResponseRedirect(reverse_lazy("book:book_index"))


def return_all_of_book(book):
    all_review = Review.objects.filter(book=book)
    for i in all_review:
        i.number_like_review = i.like_review.all().count()
        i.id_like = i.like_review.all().values_list('user_profile__user__id', flat=True)
    return all_review


def return_check_like_review(user, review):
    return LikeReview.objects.filter(user_profile=user.user_profile, review=review).exists()


def review_like(request):
    review_id = request.POST.get('review_id', False)
    book_id = request.POST.get('book_id', False)
    if review_id and request.user:
        obj, create = LikeReview.objects.get_or_create(user_profile=request.user.user_profile, review=Review.objects.get(pk=review_id))
        obj.save()
        slug_book = Book.objects.get(pk=book_id).slug
        return HttpResponseRedirect(reverse_lazy("book:book_detail", kwargs={'slug': slug_book}))
    elif request.user:
        return HttpResponseRedirect(reverse_lazy("book:book_index"))
    else:
        return HttpResponseRedirect(reverse_lazy("book:book_index"))


def review_unlike(request):
    review_id = request.POST.get('review_id', False)
    book_id = request.POST.get('book_id', False)
    if review_id and request.user:
        LikeReview.objects.get(user_profile=request.user.user_profile, review=Review.objects.get(pk=review_id)).delete()
        slug_book = Book.objects.get(pk=book_id).slug
        return HttpResponseRedirect(reverse_lazy("book:book_detail", kwargs={'slug': slug_book}))
    elif request.user:
        return HttpResponseRedirect(reverse_lazy("book:book_index"))
    else:
        return HttpResponseRedirect(reverse_lazy("book:book_index"))
