from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import Http404
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import Category, Post

from datetime import datetime

User = get_user_model()


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.filter(Q(category__is_published=True)
                                    & Q(is_published=True)
                                    & Q(pub_date__lte=datetime.now()))
    post_list = post_list[:5]
    context = {'post_list': post_list}
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
    context = {'category': category, 'post_list': post_list}
    return render(request, template, context)


def view_profile(request, username):
    template = 'blog/profile.html'
    user_profile = get_object_or_404(User, username=username)
    context = {'profile': user_profile}
    return render(request, template, context)


def create_post(request):
    pass

def edit_profile(request):
    pass
