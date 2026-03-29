from django.contrib import admin

from .models import Member, Token


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    pass


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    pass
