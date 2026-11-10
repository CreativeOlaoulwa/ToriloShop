from django.urls import path
from . import views #'.' mmeans: import from the current app package

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('hello/', views.hello_world, name='hello_world'),
]