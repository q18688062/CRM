from django.conf.urls import url
from rbac.views import role

urlpatterns = [
    url(r'^role/list/$', role.role_list, name='role_list'),
    url(r'^role/add/$', role.role_change, name='role_add'),
    url(r'^role/edit/(\d+)$', role.role_change, name='role_edit'),

    url(r'^menu/list/$', role.menu_list, name='menu_list'),
    url(r'^menu/add/$', role.menu_change, name='menu_add'),
    url(r'^menu/edit/(\d+)$', role.menu_change, name='menu_edit'),

    url(r'^permission/add/$', role.permission_change, name='permission_add'),
    url(r'^permission/edit/(\d+)$', role.permission_change, name='permission_edit'),

    url(r'^(role|permission|menu)/del/(\d+)$', role.delete, name='delete'),

    url(r'^multi/permissions/$', role.multi_permissions, name='multi_permissions'),

    url(r'^distribute/permissions/$', role.distribute_permissions, name='distribute_permissions'),
]
