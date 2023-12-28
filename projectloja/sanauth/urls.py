from django.urls import path
from sanauth import views

urlpatterns = [
    path('cadastrar/',views.cadastrar,name='cadastrar'),
    path('login/',views.handlelogin,name='handlelogin'),
]