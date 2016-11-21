from django import forms
from .models import Post, Folder
from django.contrib.auth.models import Group

class PostForm(forms.ModelForm):

    class Meta: #where we tell django which model should be used to make the form
        model = Post
        fields = ('title', 'description', 'document', 'private', 'folder') #added 'private' field

class GroupForm(forms.Form):
	group_Name = forms.CharField(max_length=250)

class FolderForm(forms.ModelForm):
	class Meta:
		model = Folder
		fields = ('name',)
