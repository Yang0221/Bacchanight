from django.contrib import admin
from django.urls import path , include
from . import views

handler404 = 'mysite.views.handler404'

urlpatterns = [
    path('' , views.home , name = 'home'),
    path('admin/', admin.site.urls),
    path('game/' , include('game.urls')),
]
