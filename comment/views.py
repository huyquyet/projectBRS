# Create your views here.
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from book.models import Book
from comment.models import CommentReview, LikeComment
from review.models import Review


def return_redirect(book_id):
    slug_book = Book.objects.get(pk=book_id).slug
    return HttpResponseRedirect(reverse_lazy("book:book_detail", kwargs={'slug': slug_book}))


def comment_create(request):
    review_id = request.POST.get('review_id', '')
    content_comment = request.POST.get('content_comment', False)
    book_id = request.POST.get('book_id', '')

    if review_id and request.user:
        obj = CommentReview.objects.create(user_profile=request.user.user_profile, review=Review.objects.get(pk=review_id.strip()))
        obj.content = content_comment
        obj.save()
        return return_redirect(book_id.strip())
    elif request.user:
        return HttpResponseRedirect(reverse_lazy("book:book_index"))
    elif book_id:
        return return_redirect(book_id.strip())
    else:
        return HttpResponseRedirect(reverse_lazy("book:book_index"))


def comment_delete(request):
    comment_id = request.POST.get('comment_id', False)
    book_id = request.POST.get('book_id', '')
    s_book_id = book_id.strip()

    if comment_id and request.user:
        obj = get_object_or_404(CommentReview, pk=comment_id)
        if request.user == obj.user_profile.user:
            obj.delete()
            return return_redirect(s_book_id)
        else:
            return HttpResponseRedirect(reverse_lazy("book:book_index"))
    elif request.user:
        return HttpResponseRedirect(reverse_lazy("book:book_index"))
    elif book_id:
        return return_redirect(s_book_id)
    else:
        return HttpResponseRedirect(reverse_lazy("book:book_index"))


def comment_review_like_unlike(request):
    comment_id = request.POST.get('comment_id', False)
    book_id = request.POST.get('book_id', False)
    check = request.POST.get('check', False)

    if comment_id and request.user and check:
        check_1 = check.strip()
        if check_1 == 'like':
            obj, create = LikeComment.objects.get_or_create(user_profile=request.user.user_profile, comment=CommentReview.objects.get(pk=comment_id))
            obj.save()
            return return_redirect(book_id.strip())
        elif check_1 == 'unlike':
            LikeComment.objects.get(user_profile=request.user.user_profile, comment=CommentReview.objects.get(pk=comment_id)).delete()
            return return_redirect(book_id.strip())
        else:
            return HttpResponseRedirect(reverse_lazy("book:book_index"))
    elif request.user:
        return HttpResponseRedirect(reverse_lazy("book:book_index"))
    else:
        return HttpResponseRedirect(reverse_lazy("book:book_index"))
