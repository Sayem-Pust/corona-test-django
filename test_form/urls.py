from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('profile_list', views.profile_list, name='profile_list'),
    path('profile_edit/<int:id>', views.profile_edit, name='profile_edit'),
    path('profile_delete/<int:id>', views.profile_delete, name='profile_delete'),
    path('profile_details', views.profile_details, name='profile_details'),
    path('login/', views.Login, name='login'),
    path('register/', views.Register, name='register'),
    path('logout/', views.Logout, name='logout'),
]
