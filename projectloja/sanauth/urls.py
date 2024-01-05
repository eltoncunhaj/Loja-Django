from django.urls import path
from sanauth import views

urlpatterns = [
    path('cadastrar/',views.cadastrar,name='cadastrar'),
    path('login/',views.handlelogin,name='handlelogin'),
    path('logout/', views.handlelogout,name='handlelogout'),
    path('activate/<uidb64>/<token>',views.ActivateContaView.as_view(),name='activate'),
    path('request-reset-email/',views.RequestResetEmailView.as_view(),name='request-reset-email'),
    path('set-novo-password/<uidb64>/<token>',views.SetNovaSenhaView.as_view(),name='set-novo-password'),
    
    
]  