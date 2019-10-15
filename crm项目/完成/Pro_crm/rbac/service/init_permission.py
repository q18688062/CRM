from django.conf import settings



def init_permission(request, obj):

    permissions = obj.roles.filter(permissions__url__isnull=False).values(
        'permissions__url',
        'permissions__url_name',
        'permissions__menu__title',
        'permissions__menu__icon',
        'permissions__menu__weight',
        'permissions__menu__id',
        'permissions__parent_id',
        'permissions__id',
        'permissions__name',
        'permissions__parent__name',
        'permissions__parent__menu_id',
    ).distinct()



    permission_dict = {}

    menu_dict = {}

    for item in permissions:
        permission_dict[item['permissions__name']] = {'url': item['permissions__url'],
                                                      'pid': item['permissions__parent_id'],
                                                      'id': item['permissions__id'],
                                                      'title': item['permissions__url_name'],
                                                      'name': item['permissions__parent__name']}

        menu_id = item.get('permissions__menu__id')
        if menu_id: #只对二级菜单放到这个里面
            if menu_id not in menu_dict:
                menu_dict[menu_id] = {
                    'title': item['permissions__menu__title'],
                    'icon': item['permissions__menu__icon'],
                    'weight': item['permissions__menu__weight'],
                    'children': [
                        {'title': item['permissions__url_name'],
                         'url': item['permissions__url'],
                         'id':item['permissions__id']}
                    ]
                }
            else:
                menu_dict[menu_id]['children'].append(
                    {'title': item['permissions__url_name'],
                     'url': item['permissions__url'],
                     'id': item['permissions__id']}
                )

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

    '''
    {
    '1': {'title': '客户管理', 'icon': 'fa-user-plus', 'weight': 10, 
    'children': [
        {'title': '我的客户', 'url': '/crm/customer_list/', 'id': 3}, 
        {'title': '公共客户', 'url': '/crm/pub_customer/', 'id': 4}, 
        {'title': '记录列表', 'url': '/crm/record_list/', 'id': 7}, 
        {'title': '报名记录', 'url': '/crm/enrollment_list/', 'id': 11}
        ]}
        }

    '''
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
    request.session[settings.MENU_SESSION_KEY] = menu_dict
    request.session[settings.STATUS_KEY] = True



