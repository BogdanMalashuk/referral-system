from django.urls import path
from . import views
from django.shortcuts import redirect


def root_redirect(request):
    return redirect('login')


urlpatterns = [
    path('', root_redirect, name='root_redirect'),
    path("login/", views.login_view, name="login"),
    path("verify/", views.verify_view, name="verify"),
    path("profile/", views.profile_view, name="profile"),
    path("activate/", views.activate_view, name="activate"),
]
