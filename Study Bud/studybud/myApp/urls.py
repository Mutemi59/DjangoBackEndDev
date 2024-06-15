
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('room/<str:pk>', views.room, name="room"),
    path('create-room', views.createRoom, name="create-room"),
    path('update-room/<int:pk>', views.updateRoom, name="update-room"),
    path('delete-room/<int:pk>', views.deleteRoom, name="delete-room"),
    path('login', views.loginPage, name = "login"),
    path('register', views.registerPage, name = "register"),
    path('profile/<str:pk>', views.userProfile, name = "profile"),
    path('logout', views.logoutUser, name = "logout"),
    path('add-comment', views.createComment, name="add-comment"),
    path('delete-comment/<int:pk>', views.deleteComment, name="delete-comment"),
    path('update-user', views.updateUser, name="update-user"),
    path('topics', views.topicsPage, name="topics"),
    path('activities', views.activitiesPage, name="activities")
]
