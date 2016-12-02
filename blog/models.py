from django.db import models
from django.contrib.auth.models import Group, User
from django.utils import timezone

class Folder(models.Model):
    name = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Document(models.Model):
    document = models.FileField(upload_to='documents/%Y/%m/%d')

class Report(models.Model): #this Report is a django model
    author = models.ForeignKey('auth.User') #link to another model
    title = models.CharField(max_length=200) #text with limited number of chars
    private = models.BooleanField(default=False) #checkbox for private                                                                           
    description = models.CharField(max_length=255, blank=True) #text with unlimited number of chars
    group = models.CharField(max_length=100, default="") 
    documents = models.ManyToManyField(Document)
    folder = models.ForeignKey(Folder, null=True, default=None, blank=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(default=timezone.now) #date and time
    published_date = models.DateTimeField(blank=True, null=True)
    #reporter = models.ForeignKey('User')
    #title = models.CharField(max_length=30)
    #sub_date = models.DateTimeField(auto_now_add=True, auto_created=True)
    #short_desc = models.TextField(max_length=30, blank=True)  # blank=True: allow empty string
    #detailed_desc = models.TextField(max_length=100, blank=True)
    #location = models.CharField(max_length=30, blank=True)
    #file = models.FileField(upload_to="reports")
    #tag = models.CharField(max_length=30, blank=True)



    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Usergroup(Group):
    users = models.ManyToManyField(User)
