from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission, Group
from django.db.models import Q #helps with querysets using "or" and "and"                                                                        
from .forms import ReportForm, GroupForm, GroupAddUser, GroupRemoveUser, FolderForm
from .models import Report, Folder, Document #.models has a . to mean current directory

@login_required
def report_list(request):
    #posts = Post.objects.all()#filter(published_date__lte=timezone.now()).order_by('published_date')
    #posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    #post = get_object_or_404(Post, pk=pk)
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
        reports = Report.objects.filter(published_date__isnull=True)
        reports = reports.filter(
            Q(title__icontains=query)|
            Q(description__icontains=query)
        )
    else:
        reports = Report.objects.filter(published_date__isnull=True).order_by('created_date') #get list of posts that have no published date (ergo, drafts)
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
        groups = Report.objects.filter(
            Q(name__icontains=query)
        )
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
        folders = Report.objects.filter(
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
            return redirect('report_list',)
    else:
        form = FolderForm()
    return render(request, 'folder/folder_new.html', {'form': form})

def folder_detail(request, pk):
    list_reports = Report.objects.all()
    folder = get_object_or_404(Folder, pk=pk)
    reports = []
    for p in list_reports:
        if p.folder == folder:
            reports.append(p)

    return render(request, 'folder/folder_detail.html', {'folder' : folder,
        'reports' : reports })

# def search_file(request):
#     if request.method == 'POST':
#         form = SearchForm(request.POST)
#         if form.is_valid():
#             # file is saved
#             title = form.cleaned_data['title']
#             desc = form.cleaned_data['description']
#             loc = form.cleaned_data['location']
#             tag = form.cleaned_data['tag']
#             r_list = Report.objects.filter(title__icontains=title).filter(
#                 Q(short_desc__icontains=desc) | Q(detailed_desc__icontains=desc)).filter(
#                 location__icontains=loc).filter(tag__icontains=tag)  # case-insensitive contain
#             context = {'report_list': r_list, 'valid': True}
#         else:
#             context = {'report_list': [], 'valid': False}
#     else:
#         form = SearchForm()
#         return render(request, 'report_search.html', {'form': form})
#     return render(request, 'report_view.html', context)
