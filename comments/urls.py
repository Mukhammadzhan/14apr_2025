from django.urls import path
from comments.views import CommentsView, AddReply
from comments.views import CommentLikeView, CommentDislikeView




urlpatterns = [
    path(route="comments/<int:pk>", view=CommentsView.as_view(), name="comments"),
    path(route="add_reply/<int:pk>", view=AddReply.as_view(), name="add_reply"),
    path("comments/<int:pk>/like/", CommentLikeView.as_view(), name="comment_like"),
    path("comments/<int:pk>/dislike/", CommentDislikeView.as_view(), name="comment_dislike"),
]