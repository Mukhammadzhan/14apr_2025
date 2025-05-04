from django.urls import path

from comments.views import CommentsView


urlpatterns = [
    path(route="comments/", view=CommentsView.as_view(), name="comments")
]
