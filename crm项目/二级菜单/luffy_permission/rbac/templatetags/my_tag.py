from django import template
from django.conf import settings
register = template.Library()


@register.inclusion_tag('rbac/menu.html')
def menu(request):
    menu = request.session.get(settings.MENU_SESSION_KEY)
    return {'menu_list': menu.values()}
