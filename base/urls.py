from django.urls import path

from . import views

urlpatterns = [

    path('', views.home_view, name = 'home'),
    path('user-profile/<str:username>/', views.user_profile_view, name = 'user-profile'),
    path('post/<str:pk>/', views.post_view, name = 'post'),
    path('explore/', views.explore_view, name = 'explore'),

    path('create/', views.create_view, name = 'create')


]
