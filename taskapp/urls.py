"""
TASK APP
"""

from django.urls import path
from taskapp import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", views.home, name='home'),
    path("home/", views.home, name='home'),
    path("login/", views.login, name="login"),
    path('signup/', views.signup, name='signup'),
]

urlpatterns += staticfiles_urlpatterns()