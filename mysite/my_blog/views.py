from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime
from bson.objectid import ObjectId
from .models import blog_collection, user_collection, user_comments


class Globals:
    user_counter = 0
    b = {"user_username": "", "user_is_authenticated": False}

    @staticmethod
    def logout_user(user):
        user = list(user_collection.find({"username": user}))[0]
        Globals.b.update({"user_username": user.get("username"), "user_is_authenticated": False})
        user_collection.update_one({"_id": ObjectId(user.get("_id"))}, {"$set": {"logged_in": False}})

    @staticmethod
    def comment(user_comment, commenter):
        if commenter:
            comment_content = {"comment": user_comment, "user": commenter}
            user_comments.insert_one(comment_content)


# Create your views here.
def index(response):
    authenticated_user = response.session.get("user_information")
    user_username = authenticated_user.get("user_username")
    if not user_username:
        Globals.user_counter += 1
        Globals.b.update({"user_username": f"user{Globals.user_counter}"})
        response.session["user_information"] = Globals.b
    if response.method == "POST":
        submit_comment = response.POST.get("comment_submit_button")
        user_comment = response.POST.get("comment_input")
        commenter = response.POST.get("comment_user")
        logout_user = response.POST.get("logout_btn")
        if submit_comment:
            Globals.comment(user_comment, commenter)
        if logout_user:
            Globals.logout_user(user_username)
            response.session["user_information"] = Globals.b
    authenticated_user = response.session.get("user_information")
    blogs = list(blog_collection.find())
    comments = list(user_comments.find())
    return render(response, "my_blog/index.html", {"blogs": blogs, "authenticated_user": authenticated_user, "comments": comments})


def about_me(response):
    authenticated_user = response.session.get("user_information")
    if response.method == "POST":
        submit_comment = response.POST.get("comment_submit_button")
        user_comment = response.POST.get("comment_input")
        commenter = response.POST.get("comment_user")
        logout_user = response.POST.get("logout_btn")
        if submit_comment:
            Globals.comment(user_comment, commenter)
        if logout_user:
            Globals.logout_user(authenticated_user.get("user_username"))
            response.session["user_information"] = Globals.b
    authenticated_user = response.session.get("user_information")    
    comments = list(user_comments.find())
    return render(response, "my_blog/about_me.html", {"comments": comments, "authenticated_user": authenticated_user})

def blogs(response, blog_id):
    _id = {"_id": ObjectId(blog_id)}
    if response.method == "POST":
        save_blog = response.POST.get("save_blog")
        edit_blog_paragraph = response.POST.get("blog_paragraph_body")
        edit_blog_title = response.POST.get("blog_title")
        logout_user = response.POST.get("logout_btn")
        if save_blog:
            if edit_blog_paragraph and edit_blog_title:
                blog_updates = {"$set": {"title": edit_blog_title, "Paragraph_body": edit_blog_paragraph}}
                blog_collection.update_one(_id, blog_updates)
        if logout_user:
            authenticated_user = response.session.get("user_information")
            Globals.logout_user(authenticated_user.get("user_username"))
            response.session["user_information"] = Globals.b
    authenticated_user = response.session.get("user_information")
    found_blog = list(blog_collection.find(_id))
    return render(response, "my_blog/blogs.html", {"blog_items": found_blog[0], "authenticated_user": authenticated_user})

def create_blog(response):
    if response.method == "POST":
        blog_body = response.POST.get("paragraph_body")
        blog_title = response.POST.get("title")
        new_blog = response.POST.get("newBlog")
        current_time = datetime.now()
        logout_user = response.POST.get("logout_btn")
        if new_blog:
            new_blog_form = {
                "title": blog_title,
                "time": current_time.strftime("%m/%d/%Y %H:%M"),
                "Paragraph_body": blog_body,
            }
            blog_collection.insert_one(new_blog_form)
            return redirect(f"/blogs/{list(blog_collection.find(new_blog_form))[0].get('_id')}")
        if logout_user:
            authenticated_user = response.session.get("user_information")
            Globals.logout_user(authenticated_user.get("user_username"))
            response.session["user_information"] = Globals.b
    authenticated_user = response.session.get("user_information")
    return render(response, "my_blog/create_blog.html", {"authenticated_user": authenticated_user})

def search(response):
    search_result = None
    if response.method == "POST":
        search_key = response.POST.get("search_bar")
        logout_user = response.POST.get("logout_btn")
        if search_key:
            # query_term = {"title": search_key}
            # search_result = list(blog_collection.find(query_term))
            search_result = list(blog_collection.aggregate([{"$search": {"index": "blog_search_index", "text": {"query": search_key, "path": {"wildcard": "*"}}}}]))
            if len(search_result) == 1:
                return redirect(f"/blogs/{search_result[0].get('_id')}/")
        if logout_user:
            authenticated_user = response.session.get("user_information")
            Globals.logout_user(authenticated_user.get("user_username"))
            response.session["user_information"] = Globals.b
    authenticated_user = response.session.get("user_information")
    return render(response, "my_blog/search.html", {"search_items": search_result, "authenticated_user": authenticated_user})

def sign_up(response):
    anon_user = response.session.get("user_information")
    if response.method == "POST":
        username = response.POST.get("user_username")
        password = response.POST.get("user_password")
        register = response.POST.get("user_submit_btn")
        if register:
            new_user = {
                "username": username,
                "password": make_password(password, salt=None, hasher="default"),
                "user_count": Globals.user_counter,
            }
            user_collection.insert_one(new_user)
            anonymous_user_comments = user_comments.find({"user": anon_user.get("user_username")})
            for comments in anonymous_user_comments:
                _id = {"_id": ObjectId(comments.get("_id"))}
                new_user_comments = {"$set": {"user": username}}
                user_comments.update_one(_id, new_user_comments)
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
                    Globals.b.update({"user_is_authenticated": True})
                    response.session["user_information"] = Globals.b
                    messages.success(response, f"{username} is now logged in! Have a nice day.")
                    return redirect("/")
                else:
                    messages.error(response, "Username or password is incorrect")
            else:
                messages.error(response, "User does not exist in our database")
    return render(response, "my_blog/sign_in.html", {"authenticate_user": authenticate_user})
