from django.urls import path
from apploja import views

urlpatterns = [
    path('',views.index,name='index'),
]
