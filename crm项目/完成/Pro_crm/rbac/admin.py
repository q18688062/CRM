from django.contrib import admin

from rbac import models


class PermissionConfig(admin.ModelAdmin):
    list_display = ['id', 'url', 'url_name']
    list_editable = ['url', 'url_name']


class RoleConfig(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_editable = ['name']


class MenuConfig(admin.ModelAdmin):
    list_display = ['id', 'title', 'weight']
    list_editable = ['weight']


admin.site.register(models.Permission, PermissionConfig)
admin.site.register(models.Role, RoleConfig)
# admin.site.register(models.User, UserConfig)
admin.site.register(models.Menu, MenuConfig)