from django.db import models
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
password = os.environ.get("MONGO_DB_PASS")

# Create your models here.
cluster = MongoClient(f"mongodb+srv://jess:{password}@cluster0.29oyw.mongodb.net/my_blog?retryWrites=true&w=majority")
db = cluster["my_blog"]
blog_collection = db["blog"]
user_collection = db["Users"]
user_comments = db["comments"]