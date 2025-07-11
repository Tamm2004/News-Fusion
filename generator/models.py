from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class userregister(models.Model):
	first_name=models.CharField(max_length=200)
	last_name=models.CharField(max_length=200)
	email=models.EmailField()
	password=models.CharField(max_length=200)

class myreview(models.Model):
	email=models.EmailField(max_length=200)
	message=models.TextField()

class helpsupport(models.Model):
	email=models.EmailField(max_length=200)
	message=models.TextField()

