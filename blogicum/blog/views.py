from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import Http404
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import Category, Post
from .forms import PostForm

from datetime import datetime
from django.utils import timezone

User = get_user_model()


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.filter(Q(category__is_published=True)
                                    & Q(is_published=True)
                                    & Q(pub_date__lte=datetime.now()))
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(Post, pk=id)
    if not post.is_published:
        raise Http404
    if not post.category.is_published:
        raise Http404
    if post.pub_date > timezone.now():
        raise Http404
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(Category, slug=category_slug)
    if not category.is_published:
        raise Http404
    post_list = Post.objects.filter(Q(category=category)
                                    & Q(is_published=True)
                                    & Q(pub_date__lte=datetime.now()))

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'category': category, 'post_list': post_list}
    context['page_obj'] = page_obj
    return render(request, template, context)


def view_profile(request, username):
    template = 'blog/profile.html'

    user_profile = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=user_profile)

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}

    context['profile'] = user_profile
    return render(request, template, context)


@login_required
def create_post(request, pk=None):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        if post.pub_date > timezone.now():
            post.is_published = False
        post.save()
        return redirect('blog:profile', username=request.user.username)
    context = {'form': form}
    return render(request, 'blog/create.html', context)


def edit_profile(request):
    pass
