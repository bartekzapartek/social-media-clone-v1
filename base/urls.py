from django.urls import path

from django.conf import settings

from django.conf.urls.static import static

from . import views

urlpatterns = [

    path('', views.home_view, name = 'home'),
    path('search/', views.search_view, name = 'search'),

    path('user-profile/<str:username>/', views.user_profile_view, name = 'user-profile'),
    path('followers/<str:username>/', views.followers_view, name = "followers"),
    path('following/<str:username>/', views.following_view, name = "following"),

    path('post/<str:pk>/', views.post_view, name = 'post'),
    path('explore/', views.explore_view, name = 'explore'),

    path('create/', views.create_view, name = 'create'),
    path('delete-post/<str:pk>/', views.delete_post_view, name = 'delete-post'),

    path('chat/<str:pk>/', views.show_chat_content, name = 'chat-content'),
    path('create-chat/', views.create_chat_room_view, name = 'create-chat'),
    path('show-chats/', views.show_chats_view, name = 'show-chats')


]

urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
