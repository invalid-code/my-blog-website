# from django.db import models
from pymongo import MongoClient

# Create your models here.
cluster = MongoClient("mongodb+srv://jess:vAUb9qC5CoC6kS3oUYEVnCcS3Uvc22Wvj9RRrt2FdBz7uqTxRNJFWC8VdHLA3ToC@cluster0.29oyw.mongodb.net/my_blog?retryWrites=true&w=majority")
db = cluster["my_blog"]
collection = db["blog"]