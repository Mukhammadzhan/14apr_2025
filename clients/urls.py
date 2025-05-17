from django.urls import path
from clients.views import (
    RegistrationView, 
    LoginView,
    ProfileView,
    ProfileUpdateView,
    ProfileDeleteView,
    ActivationView,
    ResetPasswordView,
)

app_name = 'clients'

urlpatterns = [
    path(route="reg/", view=RegistrationView.as_view(), name="reg"),
    path(route="login/", view=LoginView.as_view(), name="login"),
    path(route="profile/", view=ProfileView.as_view(), name="profile"),
    path(route="profile/edit/", view=ProfileUpdateView.as_view(), name="profile_edit"),
    path(route="profile/delete/", view=ProfileDeleteView.as_view(), name="profile_delete"),
    path(route="activation/<str:username>/<str:code>/", view=ActivationView.as_view(), name="activation"),
    path(route="reset_password/", view=ResetPasswordView.as_view(), name="reset_password"),
]