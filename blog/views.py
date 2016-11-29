from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission, Group
from django.db.models import Q #helps with querysets using "or" and "and"                                                                        
from .forms import ReportForm, GroupForm, FolderForm
from .models import Report, Folder #.models has a . to mean current directory

@login_required
def report_list(request):
    #posts = Post.objects.all()#filter(published_date__lte=timezone.now()).order_by('published_date')
    #posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    #post = get_object_or_404(Post, pk=pk)
    reports = Report.objects.filter(Q(Q(private=False) | Q(author=request.user)) & Q(published_date__lte=timezone.now())).order_by('published_date')
    return render(request, 'blog/report_list.html', {'reports': reports})

def report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)
    return render(request, 'blog/report_detail.html', {'report': report})

@login_required
def report_new(request):
    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.document = request.FILES['document']
            report.author = request.user
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
    groups = request.user.groups.all()
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
def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    return render(request, 'group/group_detail.html', {'group' : group})

@login_required
def folder_list(request):
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


