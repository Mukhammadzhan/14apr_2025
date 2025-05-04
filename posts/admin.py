from django.contrib import admin

from posts.models import Posts, Images, Categories

class PostsAdmin(admin.ModelAdmin):
    model = Posts
    list_display = ("title", "user",  "data_publication", "likes", "dislikes",)
    search_fields = ("title", "user",)
    list_per_page = 50
    list_filter = ("data_publication", "likes",)
    
admin.site.register(Posts, PostsAdmin)

class ImagesAdmin(admin.ModelAdmin):
    model = Images
    list_display = ("post", "image",)
    list_per_page = 50

admin.site.register(Images, ImagesAdmin)

class CategoriesAdmin(admin.ModelAdmin):
    model = Categories
    search_fields = ["title"]
    list_display = ["title"]
    list_per_page = 50

    

admin.site.register(Categories, CategoriesAdmin)
