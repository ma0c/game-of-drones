from django.contrib import admin
from applications.core import models
# Register your models here.


admin.site.register(models.Game)
admin.site.register(models.Player)