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
        if menu_id:
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


    #     if menu_id:
    #         if menu_id not in menu_dict:
    #             menu_dict[menu_id] = {
    #                 'title': item['permissions__menu__title'],
    #                 'icon': item['permissions__menu__icon'],
    #                 'weight': item['permissions__menu__weight'],
    #                 'children': []
    #             }
    # for item in permissions:
    #     pid = item['permissions__parent__menu_id']
    #     if pid:
    #         menu_dict[pid]['children'].append({'title': item['permissions__url_name'],
    #                  'url': item['permissions__url'],
    #                  'id': item['permissions__id']})
    # for i in menu_dict.items():
    #     print(i,'---')

    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
    request.session[settings.MENU_SESSION_KEY] = menu_dict
    request.session[settings.STATUS_KEY] = True



