from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("sign-up/", views.sign_up, name="sign up"),
    path("sign-in/", views.sign_in, name="sign in"),
    path("search/", views.search, name="search"),
    path("create-new-blog/", views.create_blog, name="create new blog"),
    path("blogs/<str:blog_id>/", views.blogs, name="blogs"),
    path("about-me/", views.about_me, name="about me"),
]