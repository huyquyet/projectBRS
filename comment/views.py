# Create your views here.
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect

from book.models import Book
from comment.models import CommentReview
from review.models import Review


def comment_create(request):
    review_id = request.POST.get('review_id', '')
    content_comment = request.POST.get('content_comment', False)
    book_id = request.POST.get('book_id', '')

    if review_id and request.user:
        obj = CommentReview.objects.create(user_profile=request.user.user_profile, review=Review.objects.get(pk=review_id))
        obj.content = content_comment
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


        # def return_all_of_book(book):
        #     all_review = Review.objects.filter(book=book)
        #     for i in all_review:
        #         i.number_like_review = i.like_review.all().count()
        #
        #     return all_review
