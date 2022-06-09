from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime
from bson.objectid import ObjectId
from .models import blog_collection, user_collection, user_comments

user_counter = 0


def comment():
    return


# Create your views here.
def index(response):
    blog_structure = list(blog_collection.find())
    if response.method == "POST":
        pass
    return render(response, "my_blog/index.html", {"blogs": blog_structure})


def about_me(response):
    return render(response, "my_blog/about_me.html", {})


def blogs(response, blog_id):
    blog_found = list(blog_collection.find({"_id": ObjectId(blog_id)}))
    if response.method == "POST":
        save_blog = response.POST.get("save_blog")
        edit_blog_paragraph = response.POST.get("blog_paragraph_body")
        edit_blog_title = response.POST.get("blog_title")
        if save_blog:
            if edit_blog_paragraph and edit_blog_title:
                _id = ObjectId(blog_id)
                blog_updates = {"$set": {"title": edit_blog_title,
                                         "Paragraph_body": edit_blog_paragraph}}
                blog_collection.update_one({"_id": _id}, blog_updates)
    return render(response, "my_blog/blogs.html", {"blog_items": blog_found[0]})


def create_blog(response):
    if response.method == "POST":
        blog_body = response.POST.get("paragraph_body")
        blog_title = response.POST.get("title")
        new_blog = response.POST.get("newBlog")
        current_time = datetime.now()
        if new_blog:
            new_blog_form = {
                "title": blog_body,
                "time": current_time.strftime("%m/%d/%Y %H:%M"),
                "Paragraph_body": blog_title,
            }
            blog_collection.insert_one(new_blog_form)
    return render(response, "my_blog/create_blog.html", {})


def search(response):
    search_term = None
    if response.method == "POST":
        search_key = response.POST.get("search_bar")
        if search_key:
            search_term = list(blog_collection.find({"title": search_key}))
    return render(response, "my_blog/search.html", {"search_items": search_term})


def sign_up(response):
    global user_counter
    if response.method == "POST":
        username = response.POST.get("user_username")
        password = response.POST.get("user_password")
        register = response.POST.get("user_submit_btn")
        if register:
            user_counter += 1
            new_user = {
            "username": username,
            "password": make_password(password, salt=None, hasher="default"),
            "user_count": user_counter,
            }
            # user_collection.insert_one(new_user)
            return redirect(f"/sign-in?username={username}")
    return render(response, "my_blog/sign_up.html", {})


def sign_in(response):
    authenticate_user = response.GET.get("username")
    if response.method == "POST":
        username = response.POST.get("user_username")
        password = response.POST.get("user_password")
        login = response.POST.get("user_login")
        u = list(user_collection.find({"username": username}))
        if login:
            if u:
                user = u[0]
                if username == user["username"] and check_password(password, user["password"]):
                    messages.success(response, f"{username} is now logged in! Have a nice day.")
                    return redirect("/")
                else:
                    messages.error(response, "Username or password is incorrect")
            else:
                messages.error(response, "User does not exist in our database")
    return render(response, "my_blog/sign_in.html", {"authenticate_user": authenticate_user})
