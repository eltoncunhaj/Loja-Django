from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('apploja.urls')),
    path('appauth/',include('appauth.urls')),
    path('sanauth/',include('sanauth.urls'))
]
