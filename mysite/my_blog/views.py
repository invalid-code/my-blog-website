from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime
from bson.objectid import ObjectId
from .models import blog_collection, user_collection, user_comments

user_counter = 0


def comment(user_comment, commenter):
    if commenter:
        comment_content = {"comment": user_comment, "user": commenter}
        user_comments.insert_one(comment_content)
    else:
        pass

# Create your views here.
def index(response):
    if response.method == "POST":
        submit_comment = response.POST.get("comment_submit_button")
        user_comment = response.POST.get("comment_input")
        commenter = response.POST.get("comment_user")
        logout_user = response.POST.get("logout_btn")
        if submit_comment:
            comment(user_comment=user_comment, commenter=commenter)
        if logout_user:
            pass
    authenticated_user = response.session.get("user_information")
    blogs = list(blog_collection.find())
    comments = list(user_comments.find())
    return render(response, "my_blog/index.html", {"blogs": blogs, "authenticated_user": authenticated_user, "comments": comments})


def about_me(response):
    if response.method == "POST":
        submit_comment = response.POST.get("comment_submit_button")
        user_comment = response.POST.get("comment_input")
        commenter = response.POST.get("comment_user")
        logout_user = response.POST.get("logout_btn")
        if submit_comment:
            comment(user_comment=user_comment, commenter=commenter)
    authenticated_user = response.session.get("user_information")
    comments = list(user_comments.find())
    return render(response, "my_blog/about_me.html", {"comments": comments, "authenticated_user": authenticated_user})

def blogs(response, blog_id):
    _id = {"_id": ObjectId(blog_id)}
    if response.method == "POST":
        save_blog = response.POST.get("save_blog")
        edit_blog_paragraph = response.POST.get("blog_paragraph_body")
        edit_blog_title = response.POST.get("blog_title")
        if save_blog:
            if edit_blog_paragraph and edit_blog_title:
                blog_updates = {"$set": {"title": edit_blog_title,
                                         "Paragraph_body": edit_blog_paragraph}}
                blog_collection.update_one(_id, blog_updates)
    found_blog = list(blog_collection.find(_id))
    return render(response, "my_blog/blogs.html", {"blog_items": found_blog[0]})

def create_blog(response):
    if response.method == "POST":
        blog_body = response.POST.get("paragraph_body")
        blog_title = response.POST.get("title")
        new_blog = response.POST.get("newBlog")
        current_time = datetime.now()
        if new_blog:
            new_blog_form = {
                "title": blog_title,
                "time": current_time.strftime("%m/%d/%Y %H:%M"),
                "Paragraph_body": blog_body,
            }
            blog_collection.insert_one(new_blog_form)
            query_blog = {"title": blog_title, "Paragraph_body": blog_body}
            blog_id = list(blog_collection.find(query_blog)).index(0).get("_id")
            return redirect(f"blogs/{blog_id}/")
    return render(response, "my_blog/create_blog.html", {})

def search(response):
    search_result = None
    if response.method == "POST":
        search_key = response.POST.get("search_bar")
        if search_key:
            # query_term = {"title": search_key}
            # search_result = list(blog_collection.find(query_term))
            search_result = list(blog_collection.aggregate([{"$search": {"index": "blog_search_index", "text": {"query": search_key, "path": {"wildcard": "*"}}}}]))
            if len(search_result) == 1:
                blog_id = search_result[0].get("_id")
                return redirect(f"/blogs/{blog_id}/")
    return render(response, "my_blog/search.html", {"search_items": search_result})

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
            user_collection.insert_one(new_user)
            return redirect(f"/sign-in?username={username}")
    return render(response, "my_blog/sign_up.html")

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
                    query_user = list(user_collection.find({"username": username}))
                    user_id = query_user[0].get("_id")
                    login_user = {"$set": {"logged_in": True}}
                    user_collection.update_one({"_id": user_id}, login_user)
                    a = {"user_username": username, "user_is_authenticated": True}
                    response.session["user_information"] = a
                    messages.success(response, f"{username} is now logged in! Have a nice day.")
                    return redirect("/")
                else:
                    messages.error(response, "Username or password is incorrect")
            else:
                messages.error(response, "User does not exist in our database")
    return render(response, "my_blog/sign_in.html", {"authenticate_user": authenticate_user})
