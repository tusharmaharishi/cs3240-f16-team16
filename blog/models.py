from django.db import models
from django.contrib.auth.models import Group, User
from django.utils import timezone

class Post(models.Model): #this post is a django model
    author = models.ForeignKey('auth.User') #link to another model
    title = models.CharField(max_length=200) #text with limited number of chars
    text = models.TextField() #text with unlimited number of chars
    created_date = models.DateTimeField(default=timezone.now) #date and time
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Usergroup(Group):
    users = models.ManyToManyField(User)