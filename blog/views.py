from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission, Group
from django.db.models import Q #helps with querysets using "or" and "and"                                                                        
from .forms import ReportForm, GroupForm, GroupAddUser, GroupRemoveUser, FolderForm, SiteManagerAdd
from .models import Report, Folder, Document #.models has a . to mean current directory
from django_messages.models import Message, MessageManager, inbox_count_for
from django.http import HttpResponse
import json
import os

@login_required
def report_list(request):
    query = request.GET.get("q")
    if query:
        reports = Report.objects.filter((
            Q(title__icontains=query)|
            Q(author__first_name__icontains=query)|
            Q(author__last_name__icontains=query)|
            Q(long_description__icontains=query)|
            Q(short_description__icontains=query)
        ) & Q(Q(private=False) | Q(author=request.user)) & Q(published_date__lte=timezone.now())) # fixing privacy issues with searching
    elif request.user.is_superuser:
        reports = Report.objects.all
    else:
        reports = Report.objects.filter(Q(Q(private=False) | Q(author=request.user)) & Q(published_date__lte=timezone.now())).order_by('published_date')
    return render(request, 'blog/report_list.html', {'reports': reports})

def report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)
    return render(request, 'blog/report_detail.html', {'report': report})

@login_required
def report_new(request):
    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')
        print(request.FILES.getlist('files'))
        if form.is_valid():
            report = form.save(commit=False)
            report.author = request.user
            report.save()
            report.group = form.cleaned_data['group']
            for file in files:
                document = Document(document=file)
                document.save()
                report.documents.add(document)
            #post.published_date = timezone.now()
            report.save()
            return redirect('report_detail', pk=report.pk)
    else:
        form = ReportForm()
    return render(request, 'blog/report_edit.html', {'form': form})

@login_required
def report_edit(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            report = form.save(commit=False)
            report.author = request.user
            #post.published_date = timezone.now()
            report.save()
            return redirect('report_detail', pk=report.pk)
    else:
        form = ReportForm(instance=report)
    return render(request, 'blog/report_edit.html', {'form': form})

@login_required
def report_draft_list(request):
    query = request.GET.get("q")
    if query:
        reports = Report.objects.filter(Q(Q(private=False) | Q(author=request.user)) & Q(published_date__isnull=True)) 
        reports = reports.filter(
            Q(Q(title__icontains=query)|
            Q(author__first_name__icontains=query)|
            Q(author__last_name__icontains=query)|
            Q(long_description__icontains=query)|
            Q(short_description__icontains=query)
            ) & Q(Q(private=False) | Q(author=request.user))) 
    else:
        reports = Report.objects.filter(Q(Q(private=False) | Q(author=request.user)) & Q(published_date__isnull=True)).order_by('created_date') #get list of posts that have no published date (ergo, drafts)
    return render(request, 'blog/report_draft_list.html', {'reports': reports})

@login_required
def report_publish(request, pk):
    report = get_object_or_404(Report, pk=pk)
    report.publish()
    return redirect('report_detail', pk=pk)

@login_required
def report_remove(request, pk):
    report = get_object_or_404(Report, pk=pk)
    report.delete() #every django model can be deleted with the .delete() method
    return redirect('report_list')


@login_required
def group_list(request):
    query = request.GET.get("q")
    if query:
        groups = Group.objects.filter(
            Q(name__icontains=query)
        )
    elif request.user.is_superuser:
        groups = Group.objects.all()
    else:
        groups = request.user.groups.all()
    
    #posts = Post.objects.filter(Q(Q(private=False) | Q(author=request.user)) & Q(published_date__lte=timezone.now())).order_by('published_date')
    return render(request, 'group/group_list.html', {'groups' : groups})

@login_required
def group_new(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group_name = form.cleaned_data['group_Name']
            group = Group.objects.create(name=group_name)
            user = request.user
            user.groups.add(group)
            return redirect('group_list',)
    else:
        form = GroupForm()
    return render(request, 'group/group_new.html', {'form': form})

@login_required
def group_adduser(request, pk):
    if request.method == "POST":
        form = GroupAddUser(request.POST)
        if form.is_valid():
            group = get_object_or_404(Group, pk=pk)
            name = form.cleaned_data['user']
            #Cannot resolve keyword 'name' into field. Choices are: date_joined, email, first_name, groups, id, is_active, is_staff, is_superuser, last_login, last_name, logentry, password, post, registrationprofile, user_permissions, usergroup, username
            try:
                user = User.objects.get(username=name)
                group.user_set.add(user)
                return redirect('group_list',)
            except User.DoesNotExist:
                return redirect('group_list',)
    else:
        form = GroupAddUser()
    return render(request, 'group/group_adduser.html', {'form': form})

@login_required
def group_removeuser(request, pk):
    if request.method == "POST":
        form = GroupRemoveUser(request.POST)
        if form.is_valid():
            group = get_object_or_404(Group, pk=pk)
            name = form.cleaned_data['user']
            try:
                user = User.objects.get(username=name)
                group.user_set.remove(user)
                return redirect('group_list',)
            except:
                return redirect('group_list',)
    else:
        form = GroupRemoveUser()
    return render(request, 'group/group_removeuser.html', {'form': form})

@login_required
def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    userlist = group.user_set.all()
    query = request.GET.get("q")
    if query:
        reports = Report.objects.filter(
            Q(title__icontains=query)|
            Q(author__first_name__icontains=query)|
            Q(author__last_name__icontains=query)|
            Q(description__icontains=query)
        )
    else:
        reports = Report.objects.filter(Q(Q(private=False) | Q(author=request.user)) & Q(published_date__lte=timezone.now())).order_by('published_date')
    return render(request, 'group/group_detail.html', {'group' : group, 'userlist' : userlist, 'reportlist' : reports})

@login_required
def folder_list(request):
    query = request.GET.get("q")
    if query:
        folder_list = Folder.objects.filter(
            Q(name__icontains=query)|
            Q(user__icontains=query)
        )
    else:
        folder_list = Folder.objects.all()
    folders = []
    for f in folder_list:
       if f.user == request.user.username:
           folders.append(f);
    return render(request, 'folder/folder_list.html', {'folders' : folders})

@login_required
def folder_new(request):
    print("Hi")
    if request.method == "POST":
        f = Folder(user=request.user.username)
        form = FolderForm(request.POST, instance=f)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.name = form.cleaned_data['name']
            #post.published_date = timezone.now()
            folder.save()
            return redirect('folder_list',)
    else:
        form = FolderForm()
    return render(request, 'folder/folder_new.html', {'form': form})

@login_required
def folder_edit(request, pk):
    print("Hi")
    folder = get_object_or_404(Folder, pk=pk)
    if request.method == "POST":
        form = FolderForm(request.POST, instance=folder)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.name = form.cleaned_data['name']
            #post.published_date = timezone.now()
            folder.save()
            return redirect('folder_list',)
    else:
        form = FolderForm()
    return render(request, 'folder/folder_edit.html', {'form': form})

def folder_detail(request, pk):
    list_reports = Report.objects.all()
    folder = get_object_or_404(Folder, pk=pk)
    reports = []
    for p in list_reports:
        if p.folder == folder:
            reports.append(p)

    return render(request, 'folder/folder_detail.html', {'folder' : folder,
        'reports' : reports })

def folder_remove(request, pk):
    folder = get_object_or_404(Folder, pk=pk)
    folder.delete() #every django model can be deleted with the .delete() method
    return redirect('folder_list')

def get_unread_messages(request):
    unread_messages = inbox_count_for(request.user)
    return HttpResponse(unread_messages)

def fda_fetch(request):
    reports = Report.objects.all()
    if "title" not in reports:
        HttpResponse("No report")
    report_name = request.POST.get("title")
    report = Report.objects.get(title=report_name)
    data_list = []
    list = report.documents.all()

    if not list.count():
        return HttpResponse(json.dumps("nothing"))

    for document in list:
        data_list.append(document.document.name)

    data = json.dumps(data_list)
    return HttpResponse(data)

def fda_fetch_all(request):
    report_list = Report.objects.filter(Q(Q(private=False) | Q(author=request.user)) & Q(published_date__lte=timezone.now())) #private=False
    if not report_list.count():
        return HttpResponse(json.dumps("No public reports"))

    list = []
    for report in report_list:
        list.append((report.title, report.short_description))

    data = json.dumps(sorted(list))
    return HttpResponse(data)
    
def fda_download(request):
    report_name = request.POST.get("title")
    report = Report.objects.get(title=report_name)
    file_name = request.POST.get("name")
    list = report.documents.all()
    for document in list:
        if file_name == document.document.name:
            return HttpResponse(document.document)
    return HttpResponse("File not found")

def fda_authenticate(request):
    if request.user.is_authenticated():
        return HttpResponse("is logged in")
    else:
        return HttpResponse("not logged in")
    #return request.user.is_authenticated()

@login_required
def add_site_manager(request):
    if request.method == "POST":
        form = SiteManagerAdd(request.POST)
        if form.is_valid():
            name = form.cleaned_data['user']
            user = User.objects.get(username=name)
            user.is_superuser = True
            user.save()
            return redirect('report_list',)
    else:
        form = SiteManagerAdd()
    return render(request, 'admin/add_site_manager.html', {'form' : form})

@login_required
def site_manager_actions(request):
    return render(request, 'admin/site_manager_actions.html',)

@login_required
def suspend_user(request):
    if request.method == "POST":
        form = SiteManagerAdd(request.POST)
        if form.is_valid():
            name = form.cleaned_data['user']
            user = User.objects.get(username=name)
            user.is_active = False
            user.save()
            return redirect('report_list',)
    else:
        form = SiteManagerAdd()
    return render(request, 'admin/suspend_user.html', {'form' : form })

@login_required
def restore_user(request):
    if request.method == "POST":
        form = SiteManagerAdd(request.POST)
        if form.is_valid():
            name = form.cleaned_data['user']
            user = User.objects.get(username=name)
            user.is_active = True
            user.save()
            return redirect('report_list',)
    else:
        form = SiteManagerAdd()
    return render(request, 'admin/restore_user.html', {'form' : form })

@login_required
def delete_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    report.delete()
    return redirect('report_list',)