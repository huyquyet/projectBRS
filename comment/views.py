# Create your views here.
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
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
    # book_id = request.POST.get('book_id', '')
    response_data = {}
    if review_id and request.user:
        obj = CommentReview.objects.create(user_profile=request.user.user_profile,
                                           review=Review.objects.get(pk=review_id.strip()))
        obj.content = content_comment
        obj.save()
        response_data['user_avata'] = obj.user_profile.avata.url
        response_data['user_id'] = obj.user_profile.user.id
        response_data['user_first_name'] = obj.user_profile.user.first_name
        response_data['user_last_name'] = obj.user_profile.user.last_name
        response_data['comment_id'] = obj.id
        response_data['book_id'] = obj.review.book.id
        response_data['date'] = obj.date
        response_data['content'] = obj.content
        response_data['date'] = obj.date
        # response_data['get_total_like'] = obj.get_total_like
        return JsonResponse(response_data)
        # return return_redirect(book_id.strip())
        # elif request.user:
        #     return HttpResponseRedirect(reverse_lazy("book:book_index"))
        # elif book_id:
        # return return_redirect(book_id.strip())
    else:
        response_data['result'] = 'error'
        return JsonResponse(response_data)


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
            obj, create = LikeComment.objects.get_or_create(user_profile=request.user.user_profile,
                                                            comment=CommentReview.objects.get(pk=comment_id))
            obj.save()
            return return_redirect(book_id.strip())
        elif check_1 == 'unlike':
            LikeComment.objects.get(user_profile=request.user.user_profile,
                                    comment=CommentReview.objects.get(pk=comment_id)).delete()
            return return_redirect(book_id.strip())
        else:
            return HttpResponseRedirect(reverse_lazy("book:book_index"))
    elif request.user:
        return HttpResponseRedirect(reverse_lazy("book:book_index"))
    else:
        return HttpResponseRedirect(reverse_lazy("book:book_index"))


def comment_review_unlike(request):
    id_comment = request.POST.get('id_comment', False)
    response_data = {}
    if id_comment:
        obj = LikeComment.objects.get(user_profile=request.user.user_profile,
                                      comment=CommentReview.objects.get(pk=id_comment))
        obj.delete()
        response_data['result'] = True
        response_data['like'] = CommentReview.objects.get(id=id_comment).get_total_like()
        return JsonResponse(response_data)
    else:
        response_data['result'] = False


def comment_review_like(request):
    id_comment = request.POST.get('id_comment', False)
    response_data = {}
    if id_comment:
        obj, create = LikeComment.objects.get_or_create(user_profile=request.user.user_profile,
                                                        comment=CommentReview.objects.get(pk=id_comment))
        obj.save()
        response_data['result'] = True
        response_data['like'] = CommentReview.objects.get(id=id_comment).get_total_like()
        return JsonResponse(response_data)
    else:
        response_data['result'] = False
