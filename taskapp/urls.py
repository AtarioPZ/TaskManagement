"""
TASK APP
"""

from django.urls import path
from taskapp import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from taskapp.views import custom_404_view

urlpatterns = [
    path("", views.home, name='home'),
    path("home/", views.home, name='home'),
    path("login/", views.user_login, name="user_login"),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_task, name='add_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path("profile/", views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('change_password/', views.change_password, name='change_password'),

]

urlpatterns += staticfiles_urlpatterns()

handler404 = custom_404_view
