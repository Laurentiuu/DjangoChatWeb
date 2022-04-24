from django.urls import path

from . import views

urlpatterns = [
    # nume la path numele functiei        
    #     |            |           
    path('', views.indexPage, name = "indexPage"),
    path('login', views.loginUser, name = "loginUser"),
    path('signup', views.newUser, name = "newUser"),
    path('index', views.indexPage, name = "indexPage"),
    path('logout', views.logoutPage, name = "logoutPage"),

    path('<str:receiver>/', views.chatRoom, name='chatRoom'),
    path('<str:receiver>/send', views.send, name='send'),



    path('userPage', views.userPage, name = "userPage"),
    path('joinRoom', views.joinRoom, name = "joinRoom"),
    # path('getMessage', views.getMessage, name = "getMessage"),

]