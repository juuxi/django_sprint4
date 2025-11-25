from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import Http404
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category, Post, Comment
from .forms import PostForm, CommentForm

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
    context['form'] = CommentForm()
    context['comments'] = Comment.objects.filter(post=post)
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
    context = {'page_obj': page_obj, 'profile': user_profile}

    return render(request, template, context)


@login_required
def create_post(request, pk=None):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', username=request.user.username)
    context = {'form': form}
    return render(request, 'blog/create.html', context)


def edit_post(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author == request.user:
        if request.POST:
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('blog:post_detail', id=id)
            
        form = PostForm(instance=post)
        context = {'form': form}
        return render(request, 'blog/create.html', context)
    
    return redirect('blog:post_detail', id=id)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        post.comment_count = post.comment_count + 1
        comment.save()
    return redirect('blog:post_detail', id=post_id)


def edit_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author == request.user:
        if request.POST:
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
                return redirect('blog:post_detail', id=post_id)
        form = CommentForm(instance=comment)
        context = {'form': form, 'comment': comment}
        return render(request, 'blog/comment.html', context)
    return redirect('blog:post_detail', id=post_id)


def delete_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id)
    context = {'comment': comment}
    if comment.author == request.user:
        if request.method == 'POST':
            comment.delete()
            post.comment_count = post.comment_count - 1
            return redirect('blog:post_detail', id=post_id)
    return render(request, 'blog/comment.html', context)


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/create.html'
    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user.username})


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    fields = ('first_name', 'last_name', 'username','email',)
    def get_object(self, queryset=None):
        return self.request.user
    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user.username})
