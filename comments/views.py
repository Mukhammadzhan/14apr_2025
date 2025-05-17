import logging

from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required

from django.views import View
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect

from comments.models import Comments
from posts.models import Posts

logger = logging.getLogger()

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse


    
class CommentsView(View):
    """Comments controller with all methods."""

    def get(self, request: HttpRequest) -> HttpResponse:
        pass

    def post(self, request: HttpRequest, pk:int) -> HttpResponse:
        client = request.user
        if not client:
            return JsonResponse(data={"error": "not authorized"})
        posts = Posts.objects.filter(id=pk)
        if not posts:
            return JsonResponse(
                data={"errror": f"Post with id {pk} not found"}
            )
        
        comment = Comments(
            post=posts[0],
            user=client,
            text=request.POST.get("text"),

        )
        comment.save()
        return redirect( "pk_post", pk=pk)

class AddReply(View):
    def post(self, request: HttpRequest, pk:int):
        client = request.user
        comments = Comments.objects.filter(id=pk)
        if not comments:
            return JsonResponse(
                data={"errror": f"Comments with id {pk} not found"}
            )

        comment = Comments(
            post=comments[0].post,
            user=client,
            parent=comments[0],
            text=request.POST.get("text"),

        )
        comment.save()
        return redirect( "pk_post", pk=comments[0].post.pk)
    

@method_decorator(csrf_exempt, name='dispatch')
class CommentLikeView(View):
    def post(self, request, pk):
        comment = Comments.objects.get(pk=pk)
        user = request.user

        if user in comment.users_disliked.all():
            comment.users_disliked.remove(user)
        if user in comment.users_liked.all():
            comment.users_liked.remove(user)
        else:
            comment.users_liked.add(user)

        comment.likes = comment.users_liked.count()
        comment.dislikes = comment.users_disliked.count()
        comment.save()

        return JsonResponse({"likes": comment.likes, "dislikes": comment.dislikes})

@method_decorator(csrf_exempt, name='dispatch')
class CommentDislikeView(View):
    def post(self, request, pk):
        comment = Comments.objects.get(pk=pk)
        user = request.user

        if user in comment.users_liked.all():
            comment.users_liked.remove(user)
        if user in comment.users_disliked.all():
            comment.users_disliked.remove(user)
        else:
            comment.users_disliked.add(user)

        comment.likes = comment.users_liked.count()
        comment.dislikes = comment.users_disliked.count()
        comment.save()

        return JsonResponse({"likes": comment.likes, "dislikes": comment.dislikes})