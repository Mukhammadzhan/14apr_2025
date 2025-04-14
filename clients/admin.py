from django.contrib import admin

from clients.models import Client

class ClientAdmin(admin.ModelAdmin):
    model = Client
    list_display = ("username", "email",  "date_created", "is_superuser")
    search_fields = ("email", "username")
    list_per_page = 50
    list_filter = ("date_created", "gender")

admin.site.register(Client, ClientAdmin)
