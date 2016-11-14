from django import forms
from .models import Post
from django.contrib.auth.models import Group

class PostForm(forms.ModelForm):

    class Meta: #where we tell django which model should be used to make the form
        model = Post
        fields = ('title', 'description', 'document')

class GroupForm(forms.Form):	
        group_Name = forms.CharField(max_length=256)
        fields = ('users')