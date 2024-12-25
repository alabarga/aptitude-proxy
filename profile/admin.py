from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Profile)

@admin.register(models.Institucion)
class InstitucionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
