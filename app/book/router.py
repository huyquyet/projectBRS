from django.template.loader import render_to_string
from swampdragon import route_handler
from swampdragon.route_handler import ModelPubRouter

from app.book.serializers import MoreCommentSerializer
from app.comment import CommentReview


class MoreCommentRouter(ModelPubRouter):
    valid_verbs = ['subscribe']
    route_name = 'commentreview'
    model = CommentReview
    serializer_class = MoreCommentSerializer

    def send_comment(self, **kwargs):
        data = render_to_string('book/comment_review.html', {'review': self.model.review, 'comment': self.model})
        self.send(data)



route_handler.register(MoreCommentRouter)
