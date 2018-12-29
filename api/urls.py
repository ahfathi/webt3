from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('v1/login/', views.Login.as_view(), name='login'),
    path('v1/tweet/', views.Tweet.as_view(), name='tweet1'),
    path('v2/tweet/', views.Tweet.as_view(), name='tweet2'),
]