from django.shortcuts import render
from .models import collection
from datetime import datetime
from bson.objectid import ObjectId

# Create your views here.
def index(response):
    if response.method == "POST":
        blog_body = response.POST.get("paragraph_body")
        blog_title = response.POST.get("title")
        new_blog = response.POST.get("newBlog")
        current_time = datetime.now()

        save_blog = response.POST.get("save_blog")
        edit_blog_id = response.POST.get("blog_id")
        edit_blog_title = response.POST.get("blog_title")
        edit_blog_paragraph = response.POST.get("blog_paragraph_body")

        if new_blog:
            new_blog_form = {
            "title": blog_body,
            "time": current_time.strftime("%m/%d/%Y %H:%M"),
            "Paragraph_body": blog_title,
        }
            collection.insert_one(new_blog_form)
        if save_blog:
            if edit_blog_paragraph or edit_blog_title:
                _id = ObjectId(edit_blog_id)
                blog_updates = {"$set": {"title": edit_blog_title, "Paragraph_body": edit_blog_paragraph}}
                collection.update_one({"_id":_id}, blog_updates)
    blogs = collection.find()
    blog_structure = []
    for blog in blogs:
        blog_structure.append(blog)
    return render(response, "my_blog/index.html", {"blogs": blog_structure})

def about_me(response):
    return render(response, "my_blog/about_me.html", {})

def blogs(response, blog_id):
    return render(response, "my_blog/blogs.html", {})

def create_blog(response):
    return render(response, "my_blog/create_blog.html", {})