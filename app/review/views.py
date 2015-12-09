# Create your views here.
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404

from app.activity.function import create_activity
from app.book.models import Book
from app.review.models import Review, LikeReview


def return_redirect(book_id):
    slug_book = Book.objects.get(pk=book_id).slug
    return HttpResponseRedirect(reverse_lazy("book:book_detail", kwargs={'slug': slug_book}))


def review_create(request):
    book_id = request.POST.get('book_id', False)
    content_review = request.POST.get('content_review', False)

    if book_id and request.user:
        obj = Review.objects.create(user_profile=request.user.user_profile,
                                    book=Book.objects.get(pk=book_id))
        obj.content = content_review
        obj.save()

        """ Install activity in database """
        create_activity(request.user.pk, 'write_review', book_id,
                        'Write review  :' + Book.objects.get(pk=book_id).title)

        return return_redirect(book_id.strip())
    elif request.user:
        return HttpResponseRedirect(reverse_lazy("book:book_index"))
    elif book_id:
        return return_redirect(book_id.strip())
    else:
        return HttpResponseRedirect(reverse_lazy("book:book_index"))


def review_update(request):
    review_id = request.POST.get('review_id', '')
    review_content = request.POST.get('review_content', False)
    book_id = request.POST.get('book_id', '')
    s_review_id = review_id.strip()
    s_book_id = book_id.strip()

    if review_id and request.user:
        obj, create = Review.objects.get_or_create(pk=s_review_id)
        obj.content = review_content
        obj.save()
        return return_redirect(s_book_id)
    elif request.user:
        return HttpResponseRedirect(reverse_lazy("book:book_index"))
    elif book_id:
        return return_redirect(s_book_id)
    else:
        return HttpResponseRedirect(reverse_lazy("book:book_index"))


def review_delete(request):
    review_id = request.POST.get('review_id', '')
    book_id = request.POST.get('book_id', '')
    s_book_id = book_id.strip()

    if review_id and request.user:
        s_review_id = review_id.strip()
        obj = get_object_or_404(Review, pk=s_review_id)
        obj.delete()
        return return_redirect(s_book_id)
    elif request.user:
        return HttpResponseRedirect(reverse_lazy("book:book_index"))
    elif book_id:
        return return_redirect(s_book_id)
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
    user_id = request.POST.get('user_id', False)
    response_data = {}
    if review_id and request.user:
        obj, create = LikeReview.objects.get_or_create(user_profile=User.objects.get(id=user_id).user_profile,
                                                       review=Review.objects.get(pk=review_id))
        obj.save()
        try:
            """ Install activity in database """
            create_activity(request.user.pk, 'like_review', review_id,
                            'Like review ' + Review.objects.get(pk=review_id).content)
        except:
            pass
        response_data['result'] = True
        response_data['like'] = Review.objects.get(id=review_id).like_review.all().count()
        return JsonResponse(response_data)
    elif request.user:
        response_data['result'] = False
        return JsonResponse(response_data)
    else:
        response_data['result'] = False
        return JsonResponse(response_data)


def review_unlike(request):
    review_id = request.POST.get('review_id', False)
    user_id = request.POST.get('user_id', False)
    response_data = {}
    if review_id and request.user:
        obj = LikeReview.objects.get(user_profile=User.objects.get(id=user_id).user_profile,
                                     review=Review.objects.get(pk=review_id))
        obj.delete()
        response_data['result'] = True
        response_data['like'] = Review.objects.get(id=review_id).like_review.all().count()
        return JsonResponse(response_data)
    elif request.user:
        response_data['result'] = False
        return JsonResponse(response_data)
    else:
        response_data['result'] = False
        return JsonResponse(response_data)


def return_list_review_of_user(user):
    list_review = Review.objects.filter(user_profile=user.user_profile).order_by('-date')
    for i in list_review:
        i.point_rating = i.book.get_rating_book()
        i.rating = i.book.rating_book.count()
        i.review = i.book.review_book.count()
        i.number_like_review = i.like_review.all().count()
        i.number_comment_review = i.comment.all().count()
    return list_review
