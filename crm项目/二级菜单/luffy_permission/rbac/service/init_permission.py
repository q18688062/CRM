from django.conf import settings

def init_permission(request,obj):

    permissions = obj.roles.filter(permissions__url__isnull=False).values(
        'permissions__url',
        'permissions__url_name',
        'permissions__menu__title',
        'permissions__menu__icon',
        'permissions__menu__id'
    ).distinct()


    permission_list = []

    menu_dict = {}

    for item in permissions:
        permission_list.append({'url': item['permissions__url']})
        menu_id = item.get('permissions__menu__id')
        if menu_id:
            if menu_id not in menu_dict:
                menu_dict[menu_id] = {
                    'title': item['permissions__menu__title'],
                    'icon': item['permissions__menu__icon'],
                    'children': [
                        {'title': item['permissions__url_name'],
                        'url': item['permissions__url']}
                    ]
                }
            else:
                menu_dict[menu_id]['children'].append(
                    {'title': item['permissions__url_name'],
                     'url': item['permissions__url']}
                )


    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    request.session[settings.MENU_SESSION_KEY] = menu_dict
    request.session[settings.STATUS_KEY] = True



