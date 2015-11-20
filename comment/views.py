# Create your views here.

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from book.models import Book
from comment.models import CommentReview, LikeComment
from review.models import Review


def return_redirect(book_id):
    slug_book = Book.objects.get(pk=book_id).slug
    return HttpResponseRedirect(reverse_lazy("book:book_detail", kwargs={'slug': slug_book}))


def comment_create(request):
    review_id = request.POST.get('review_id', '')
    content_comment = request.POST.get('content_comment', False)
    response_data = {}
    if review_id and request.user:
        obj = CommentReview.objects.create(user_profile=request.user.user_profile,
                                           review=Review.objects.get(pk=review_id.strip()))
        obj.content = content_comment
        obj.save()
        html = render_to_string('book/comment_review.html', {'review': obj.review, 'comment': obj})
        res = {'html': html}
        return JsonResponse(res)
    else:
        response_data['result'] = 'error'
        return JsonResponse(response_data)


def comment_delete(request):
    comment_id = request.POST.get('comment_id', False)
    response_data = {}
    if comment_id and request.user:
        obj = get_object_or_404(CommentReview, pk=comment_id)
        if request.user == obj.user_profile.user:
            obj.delete()
            response_data['result'] = 'Delete Successfull'
            return JsonResponse(response_data)
        else:
            response_data['result'] = 'Denied Permission'
            return JsonResponse(response_data)
    else:
        response_data['result'] = 'Error '
        return JsonResponse(response_data)


# def comment_review_like_unlike(request):
#     comment_id = request.POST.get('comment_id', False)
#     book_id = request.POST.get('book_id', False)
#     check = request.POST.get('check', False)
#
#     if comment_id and request.user and check:
#         check_1 = check.strip()
#         if check_1 == 'like':
#             obj, create = LikeComment.objects.get_or_create(user_profile=request.user.user_profile,
#                                                             comment=CommentReview.objects.get(pk=comment_id))
#             obj.save()
#             return return_redirect(book_id.strip())
#         elif check_1 == 'unlike':
#             LikeComment.objects.get(user_profile=request.user.user_profile,
#                                     comment=CommentReview.objects.get(pk=comment_id)).delete()
#             return return_redirect(book_id.strip())
#         else:
#             return HttpResponseRedirect(reverse_lazy("book:book_index"))
#     elif request.user:
#         return HttpResponseRedirect(reverse_lazy("book:book_index"))
#     else:
#         return HttpResponseRedirect(reverse_lazy("book:book_index"))
#

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


def load_more_comment(request):
    review_id = request.POST.get('review_id', False)
    start = request.POST.get('start', False)
    end = request.POST.get('end', False)
    number_comment = request.POST.get('number_comment', False)
    response_data = {}
    if int(end) < int(number_comment):
        comments = CommentReview.objects.filter(review__id=review_id).order_by('-id')[int(start):int(end)]
    else:
        comments = CommentReview.objects.filter(review=Review.objects.get(id=review_id)).order_by('-id')[
                   int(start):int(number_comment)]
    for i in range(len(comments)):
        response_data[str(i)] = load_one_comment(comments[i].id)
    return JsonResponse(response_data)

    # review_id = request.POST.get('review_id', False)
    # start = request.POST.get('start', False)
    # end = request.POST.get('end', False)
    # number_comment = request.POST.get('number_comment', False)
    # response_data = []
    # # number_comment = CommentReview.objects.filter(review=Review.objects.get(id=review_id)).count()
    # if int(end) < int(number_comment):
    #     review = Review.objects.get(id=review_id)
    #     comments = CommentReview.objects.filter(review__id=review_id).order_by('-id')[int(start):int(end)]
    # else:
    #     comments = CommentReview.objects.filter(review=Review.objects.get(id=review_id)).order_by('-id')[
    #                int(start):int(number_comment)]
    # for i in range(len(comments)):
    #     response_data.append(load_one_comment(comments[i].id))
    # data = {
    #     'data': response_data
    # }
    # return JsonResponse(data)


def load_one_comment(id_comment):
    response_data = {}
    obj = CommentReview.objects.get(id=id_comment)
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
    return response_data
