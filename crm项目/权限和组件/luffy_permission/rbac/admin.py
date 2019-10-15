from django.contrib import admin

from rbac import models


class PermissionConfig(admin.ModelAdmin):
    list_display = ['id', 'url', 'url_name']
    list_editable = ['url', 'url_name']


class RoleConfig(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_editable = ['name']


class UserConfig(admin.ModelAdmin):
    list_display = ['id', 'username']
    list_editable = ['username']



admin.site.register(models.Permission, PermissionConfig)
admin.site.register(models.Role, RoleConfig)
admin.site.register(models.User, UserConfig)