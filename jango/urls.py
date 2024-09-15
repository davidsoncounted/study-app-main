from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name= 'register'), 
    path('login', views.loginPage, name= 'login'),
    path('logout', views.logoutPage, name= 'logout'),
    path('', views.Home, name = 'home'),
    path('room/<str:pk>/', views.room, name = 'room'),
    path('room-form', views.createRoom, name= 'room-form'),
    path('profile/<str:pk>/', views.userProfile, name= 'user-profile'),
    path('update-form/<str:pk>/', views.updateRoom, name= 'update-form'),
    path('delete-room/<str:pk>/', views.deleteRoom, name= 'delete-room'),
    path('delete-message/<str:pk>/', views.deleteMessage, name= 'delete-message'),
    path('delete-recent/<str:pk>/', views.deleteRecent, name= 'delete-recent'),
    path('update-user/', views.updateUser, name= 'update-user'),
    path('topics', views.topicPage, name= 'topics'),
    path('activity', views.activityPage, name= 'activity')

]