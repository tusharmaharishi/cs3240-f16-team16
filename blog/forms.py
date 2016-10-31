from django import forms
from .models import Post

class PostForm(forms.ModelForm):

    class Meta: #where we tell django which model should be used to make the form
        model = Post
        fields = ('title', 'text',)
