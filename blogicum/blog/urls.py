from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.post_detail, name='post_detail'),
    path('profile/<str:username>/', views.view_profile, name='profile'),
    path('create/', views.create_post, name='create_post'),
    path('<slug:category_slug>/', views.category_posts, name='category_posts'),
    path('', views.edit_profile, name='edit_profile'),
]
