import re
from django import template
from django.conf import settings
from collections import OrderedDict
register = template.Library()


@register.inclusion_tag('rbac/menu.html')
def menu(request):
    order_dic = OrderedDict()
    menu_list = request.session.get(settings.MENU_SESSION_KEY)
    key_num = sorted(menu_list, key=lambda x: menu_list[x]['weight'], reverse=True)
    for key in key_num:
        order_dic[key] = menu_list[key]

    for item in menu_list.values():
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

