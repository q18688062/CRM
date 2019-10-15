from django import template
from django.urls import reverse
from django.http.request import QueryDict
from django.utils.safestring import mark_safe

mark_safe
register = template.Library()

@register.simple_tag
def reverse_url(request, name, *args, **kwargs):
    next = request.get_full_path()
    res_dic = QueryDict(mutable=True)
    url = reverse(name, args=args, kwargs=kwargs)
    res_dic['next'] = next
    res_url = '{}?{}'.format(url, res_dic.urlencode())
    return res_url


