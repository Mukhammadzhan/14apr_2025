from django.urls import path
from posts.views import PostsView, BasePostView, EditPostView, delete_post, LikesView

urlpatterns = [
    path("", BasePostView.as_view(), name="base"),
    path("post_form", PostsView.as_view(), name="post_form"),
    path("post/<int:pk>", EditPostView.as_view(), name="pk_post"),
    path("post/<int:pk>/edit/", EditPostView.as_view(), name="edit_post"),
    path("post/<int:post_id>/delete/", delete_post, name="delete_post"),  
    path(route="post/<int:pk>/<str:action>", 
        view=LikesView.as_view(), name="likes_view"
    )
]
