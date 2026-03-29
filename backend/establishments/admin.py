from django.contrib import admin

from .models import Establishment, Manage, Table


@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    pass


@admin.register(Manage)
class ManageAdmin(admin.ModelAdmin):
    pass
