"""
TASK APP
"""

from django.urls import path
from taskapp import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", views.home, name='home'),
    path("home/", views.home, name='home'),
    path("login/", views.user_login, name="user_login"),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

urlpatterns += staticfiles_urlpatterns()