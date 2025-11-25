from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.post_detail, name='post_detail'),
    path('profile/<str:username>/', views.view_profile, name='profile'),
    path('create/', views.create_post, name='create_post'),
    path('<int:id>/edit/', views.edit_post, name='edit_post'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete_post'),
    path('', views.edit_profile, name='edit_profile'),
    path('<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('<int:post_id>/edit_comment/<int:comment_id>', views.edit_comment, name='edit_comment'),
    path('<int:post_id>/delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('<slug:category_slug>/', views.category_posts, name='category_posts'),
]
