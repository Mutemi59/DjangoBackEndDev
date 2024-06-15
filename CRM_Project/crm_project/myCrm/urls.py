from django.urls import path
from . import views

urlpatterns = [
    path('', views.signIn, name="signIn"),
    path('home', views.home, name="home"),
    path('signUp', views.signUp, name="signUp"),
    path('add_record', views.addRecord, name="add_record"),
    path('logOut', views.logOut, name="logOut"),
    path('update/<int:pk>', views.update, name="update")
]

