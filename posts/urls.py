from django.urls import path
from posts.views import PostsView, BasePostView, EditPostView, delete_post, LikesView, PostView
from clients.views import (
    ProfileView,
    ProfileUpdateView,
    ProfileDeleteView,
)


urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
    path("profile/delete/", ProfileDeleteView.as_view(), name="profile_delete"),

    path("", BasePostView.as_view(), name="base"),
    path("post_form", PostsView.as_view(), name="post_form"),
    path("post/<int:pk>", PostView.as_view(), name="pk_post"),
    path("post/<int:pk>/edit/", EditPostView.as_view(), name="edit_post"),
    path("post/<int:post_id>/delete/", delete_post, name="delete_post"),
    path("post/<int:pk>/<str:action>", LikesView.as_view(), name="likes_view"),
]
