import re
from django import template
from django.conf import settings
from collections import OrderedDict
register = template.Library()


@register.inclusion_tag('rbac/menu.html')
def menu(request):
    order_dic = OrderedDict()
    menu_list = request.session.get(settings.MENU_SESSION_KEY)
    '''
    {'1': {'title': '客户管理', 'icon': 'fa-user-plus', 'weight': 10,
           'children': [{'title': '我的客户', 'url': '/crm/customer_list/', 'id': 3},
                        {'title': '公共客户', 'url': '/crm/pub_customer/', 'id': 4},
                        {'title': '记录列表', 'url': '/crm/record_list/', 'id': 7},
                        {'title': '报名记录', 'url': '/crm/enrollment_list/', 'id': 11}]},
     '2': {'title': '班级管理', 'icon': 'fa-users', 'weight': 9,
           'children': [{'title': '班级列表', 'url': '/crm/class_list/', 'id': 15}]},
     '3': {'title': '权限管理', 'icon': 'fa-paper-plane', 'weight': 5,
           'children': [{'title': '角色管理', 'url': '/rbac/role/list/', 'id': 22},
                        {'title': '菜单管理', 'url': '/rbac/menu/list/', 'id': 25},
                        {'title': '批量添加权限', 'url': '/rbac/multi/permissions/', 'id': 31},
                        {'title': '分配权限', 'url': '/rbac/distribute/permissions/', 'id': 32}]}}
'''
    key_num = sorted(menu_list, key=lambda x: menu_list[x]['weight'], reverse=True)
    for key in key_num:
        order_dic[key] = menu_list[key]

    for item in menu_list.values():  #容器类型 指向同一地址 先后顺序无所谓
        item['class'] = 'hide'
        for i in item['children']:
            if i['id'] == request.current_menu_id:
            # if re.match(r'{}$'.format(i['url']), request.get_full_path()):
                i['class'] = 'active'
                item['class'] = ''

    return {'menu_list': order_dic.values()}


@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    breadcrumb_list = request.breadcrumb_list
    return {'breadcrumb_list': breadcrumb_list}


@register.filter
def is_include(request, target):
    permission = request.session.get(settings.PERMISSION_SESSION_KEY)
    if target in permission:
        return True


@register.simple_tag
def gen_role_url(request, rid):
    params = request.GET.copy()
    params['rid'] = rid
    return params.urlencode()
