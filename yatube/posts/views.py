from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


def index(request):
    template_main = 'posts/index.html'
    posts = Post.objects.all()
    page = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = page.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template_main, context)


def group_posts(request, slug):
    template_group = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    page = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = page.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'group': group
    }
    return render(request, template_group, context)


def profile(request, username):
    template_name = 'posts/profile.html'
    author = User.objects.get(username=username)
    profile = author.posts.all()
    page = Paginator(profile, 10)
    page_number = request.GET.get('page')
    page_obj = page.get_page(page_number)
    post_count = Post.objects.filter(author__username=username).count()
    context = {
        'page_obj': page_obj,
        'post_count': post_count,
        'author': author
    }
    return render(request, template_name, context)


def post_detail(request, post_id):
    template_name = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    author = get_object_or_404(User, id=post.author_id)
    post_count = Post.objects.filter(author=author).count()
    context = {
        'post': post,
        'post_count': post_count,
        'author': author
    }
    return render(request, template_name, context)


@login_required
def post_create(request):
    template_name = 'posts/create_post.html'
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=post.author)
    context = {
        'form': form
    }
    return render(request, template_name, context)


@login_required
def post_edit(request, post_id):
    template_name = 'posts/create_post.html'
    post = Post.objects.get(pk=post_id)
    form = PostForm(request.POST, instance=post)
    is_edit = post
    if request.user == post.author:
        if form.is_valid():
            post = form.save()
            post.author = request.user
            post.save()
            return redirect('posts:post_detail', post_id)
        context = {
            'form': form,
            'is_edit': is_edit,
            'post': post
        }
        return render(request, template_name, context)
    return redirect('posts:post_detail', post_id)
