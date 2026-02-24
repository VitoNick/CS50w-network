
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("modal/new-post", views.get_modal_content, name="get_modal_content"),
    path("post/create", views.create_post, name="create_post")
]
