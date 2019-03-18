from django.contrib import admin
from applications.core import models
# Register your models here.


admin.site.register(models.Player)
admin.site.register(models.Game)
admin.site.register(models.Round)
admin.site.register(models.GameType)
admin.site.register(models.GameMove)
admin.site.register(models.MoveResult)
