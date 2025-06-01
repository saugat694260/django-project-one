
from django.urls import path
from django.contrib.auth import views 
from .import views
app_name='users_app'

urlpatterns=[
    
    path('', views.UserList.as_view(), name='users'),
    path('users/messages/<str:username>/', views.UserMessages.as_view(), name='user_messages'),

]