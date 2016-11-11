from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission, Group
from .forms import PostForm, GroupForm
from .models import Post #.models has a . to mean current directory

def post_list(request):
    #posts = Post.objects.all()#filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    #post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date') #get list of posts that have no published date (ergo, drafts)
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete() #every django model can be deleted with the .delete() method
    return redirect('post_list')

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


