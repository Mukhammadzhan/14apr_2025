import logging
from typing import Literal

from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator


from django.views import View
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.utils import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin

from posts.models import Posts, Images, Categories

logger = logging.getLogger()

class BasePostView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        is_active = request.user.is_active
        posts: QuerySet[Posts] = Posts.objects.all()
        return render(
            request=request, 
            template_name="posts.html", 
            context={
                "posts": posts,
                "user": is_active       
            }
        )

class PostsView(View):
    """Posts controller with all methods."""

    def get(self, request: HttpRequest) -> HttpResponse:
        is_active = request.user.is_active
        categories = Categories.objects.all()
        if not is_active:
            return redirect(to="login")
        return render(
            request=request, 
            template_name="post_form.html", 
            context={"categories": categories}
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        post = Posts.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            description=request.POST.get("description")
        )
        post.categories.set(request.POST.getlist("categories"))
        imgs = [Images(image=img, post=post) 
                for img in request.FILES.getlist("images")]
        Images.objects.bulk_create(imgs)
        return redirect(to="base")

class PostView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        try:
            post = Posts.objects.get(pk=pk)
        except Posts.DoesNotExist: 
            return HttpResponse("<h1>Пост не найден</h1>", status=404)

        categories = Categories.objects.all()
        return render(
            request=request, 
            template_name="pk_post.html", 
            context={"post": post, "categories": categories, "request": request}
        )

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        try:
            post = Posts.objects.get(pk=pk)
        except Posts.DoesNotExist:
            return HttpResponse("<h1>Пост не найден</h1>", status=404)

        if request.user != post.user:
            return HttpResponse("<h2>У вас нет прав редактировать этот пост</h2>", status=403)

        # Обновляем заголовок и описание
        post.title = request.POST.get("title", post.title)
        post.description = request.POST.get("description", post.description)

        # Обновляем категории
        category_ids = request.POST.getlist("categories")
        if category_ids:
            post.categories.set(category_ids)

        # Добавляем новые изображения, если они есть
        images = request.FILES.getlist("images")
        if images:
            from posts.models import Images  # убедитесь, что модель импортирована
            new_images = [Images(image=img, post=post) for img in images]
            Images.objects.bulk_create(new_images)

        post.save()

        # Перенаправляем на просмотр поста после редактирования
        return redirect("edit_post", pk=post.pk)

class EditPostView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        try:
            post = Posts.objects.get(pk=pk)
        except Posts.DoesNotExist: 
            return HttpResponse("<h1>Пост не найден</h1>", status=404)

        categories = Categories.objects.all()
        return render(
            request=request, 
            template_name="edit_post.html", 
            context={"post": post, "categories": categories, "request": request}
        )

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        try:
            post = Posts.objects.get(pk=pk)
        except Posts.DoesNotExist:
            return HttpResponse("<h1>Пост не найден</h1>", status=404)

        if request.user != post.user:
            return HttpResponse("<h2>У вас нет прав редактировать этот пост</h2>", status=403)

        # Обновляем заголовок и описание
        post.title = request.POST.get("title", post.title)
        post.description = request.POST.get("description", post.description)

        # Обновляем категории
        category_ids = request.POST.getlist("categories")
        if category_ids:
            post.categories.set(category_ids)

        # Добавляем новые изображения, если они есть
        images = request.FILES.getlist("images")
        if images:
            from posts.models import Images  # убедитесь, что модель импортирована
            new_images = [Images(image=img, post=post) for img in images]
            Images.objects.bulk_create(new_images)

        post.save()

        # Перенаправляем на просмотр поста после редактирования
        return redirect("edit_post", pk=post.pk)
    
class LikesView(LoginRequiredMixin, View):
    def post(self, request, pk, action):
        try:
            post = Posts.objects.get(pk=pk)
        except Posts.DoesNotExist:
            return JsonResponse({'error': 'Пост не найден'}, status=404)

        user = request.user
        response_data = {
            'likes': post.likes,
            'dislikes': post.dislikes,
            'action': action,
            'status': None
        }

        if action == 'like':
            if user in post.users_disliked.all():
                post.users_disliked.remove(user)
                post.dislikes -= 1

            if user in post.users_liked.all():
                post.users_liked.remove(user)
                post.likes -= 1
                response_data['status'] = 'unliked'
            else:
                post.users_liked.add(user)
                post.likes += 1
                response_data['status'] = 'liked'

        elif action == 'dislike':
            if user in post.users_liked.all():
                post.users_liked.remove(user)
                post.likes -= 1

            if user in post.users_disliked.all():
                post.users_disliked.remove(user)
                post.dislikes -= 1
                response_data['status'] = 'undisliked'
            else:
                post.users_disliked.add(user)
                post.dislikes += 1
                response_data['status'] = 'disliked'

        post.save()
        response_data.update({
            'likes': post.likes,
            'dislikes': post.dislikes
        })
        return JsonResponse(response_data)




    
@require_POST
def delete_post(request: HttpRequest, post_id: int) -> HttpResponse:
    post = Posts.objects.filter(pk=post_id).first()
    if post:
        if request.user == post.user:
            post.delete()
            messages.success(request, "Пост успешно удален.")
            return redirect('base')
        else:
            messages.error(request, "Вы не можете удалить этот пост.")
            return redirect('post_detail', post_id=post.id)
    return redirect('base')

