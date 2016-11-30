from django import forms
from .models import Report, Folder
from django.contrib.auth.models import Group

class ReportForm(forms.ModelForm):

    class Meta: #where we tell django which model should be used to make the form
        model = Report
        fields = ('title', 'description', 'document', 'private', 'folder') #added 'private' field

class GroupForm(forms.Form):
	group_Name = forms.CharField(max_length=250)

class FolderForm(forms.ModelForm):
	class Meta:
		model = Folder
		fields = ('name',)


# class SearchForm(forms.Form):
#     title = forms.CharField(max_length=30,required=False)
#     sub_date = forms.DateTimeField(label='submission date',required=False)
#     description = forms.CharField(max_length=100,required=False)
#     location = forms.CharField(max_length=30,required=False)
#     tag = forms.CharField(max_length=30,required=False)
