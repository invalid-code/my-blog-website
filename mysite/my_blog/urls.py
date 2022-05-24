from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create-new-blog/", views.create_blog, name="create new blog"),
    path("<str:blog_id>/", views.blogs, name="blogs"),
    path("about-me/", views.about_me, name="about me"),
]