from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name = "home"),
    path('zaloguj/', views.zaloguj, name = "zaloguj"),
    path('wyloguj/', views.wyloguj, name = "wyloguj"),
    path('rejestracja/', views.rejestracja, name = "rejestracja"),
    path('mojekonto/<str:pk>/', views.mojekonto, name = "mojekonto"),
    path('umow_wizyte/', views.umow_wizyte, name = "umowwizyte"),
    path('kontakt/', views.kontakt, name = "kontakt"),
    path('room/<str:pk>/', views.room, name = "room"),
    path('wszyscypsycholodzy/', views.wszyscypsycholodzy, name = "wszyscypsycholodzy"),
    path('rejestracjapsycholog/', views.rejestracjapsycholog, name="rejestracjapsycholog"),
    path('rejestracjaklient/', views.rejestracjaklient, name="rejestracjaklient"),
    path('mojekontopsycholog/', views.mojekontopsycholog, name = "mojekontopsycholog"),
    path('cennik/', views.cennik, name = "cennik"),
    path('forum/', views.forum, name="forum"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
]


