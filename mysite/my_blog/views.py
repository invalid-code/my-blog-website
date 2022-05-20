from django.shortcuts import render
from .models import collection, db
from datetime import datetime

# Create your views here.
def index(response):
    if response.method == "POST":
        blog_body = response.POST.get("paragraph_body")
        blog_title = response.POST.get("title")
        new_blog = response.POST.get("newBlog")
        edit_blog = response.POST.get("newBlog")
        if new_blog:
            current_time = datetime.now()
            new_blog = {
            "title": blog_body,
            "time": current_time.strftime("%m/%d/%Y %H:%M"),
            "Paragraph body": blog_title,
        }
            collection.insert_one(new_blog)
        elif edit_blog:
            pass
    blogs = collection.find()
    blog_structure = []
    for blog in blogs:
        blog_structure.append([db_item for db_item in blog.values()])
    return render(response, "my_blog/index.html", {"blogs": blog_structure})

def about_me(response):
    return render(response, "my_blog/about_me.html", {})