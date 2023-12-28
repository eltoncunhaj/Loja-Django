from django.urls import path
from appauth import views

urlpatterns = [
    path('a/',views.a,name='a')
]

