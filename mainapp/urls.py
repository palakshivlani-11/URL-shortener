from django.contrib import admin
from django.urls import path, include

from mainapp.views import deleteshortcuts, filtershortcuts, listshortcuts
from .views import *


urlpatterns = [
    path('register', signup, name="signup"),
    path('login',login,name="signin"),
    #path('<str:shortened_part>', redirect_url_view, name='redirect'),
    path('listshortcuts',listshortcuts,name="listshortcuts"),
    path('deleteshortcuts',deleteshortcuts,name="deleteshortcuts"),
    path('filtershortcuts',filtershortcuts,name="filtershortcuts"),
]