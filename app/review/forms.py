from django.forms import ModelForm

from app.review.models import Review

__author__ = 'FRAMGIA\nguyen.huy.quyet'


class CreateReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['content']
