import imp
from django.contrib import admin

from mainapp.models import shortcut
from .models import *

admin.site.register(shortcut)

# Register your models here.
