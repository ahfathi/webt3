from django.urls import path
from django.views.generic import ListView
from .models import Post
from . import views

app_name = 'twitter'

urlpatterns = [
	path('', ListView.as_view(template_name='twitter/index.html', model=Post, context_object_name='posts'), name='index'),
	path('new_post/', views.new_post, name='new_post'),
]