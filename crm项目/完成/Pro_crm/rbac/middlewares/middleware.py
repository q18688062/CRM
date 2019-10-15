import re
from django.conf import settings

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, reverse, HttpResponse


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        path = request.path_info
        for item in settings.WHITE_LIST:
            if re.match(item, path):
                return
        request.current_menu_id = None

        request.breadcrumb_list = [
            {'title': '首页', 'url': '/crm/index/'}
        ]

        status = request.session.get(settings.STATUS_KEY)
        if status:
            for item in settings.NO_PERMISSION_LIST:
                if re.match(item, path):
                    return
        else:
            return redirect(reverse('login'))

        permission = request.session.get(settings.PERMISSION_SESSION_KEY)
        for item in permission.values():
            if re.match(r'{}$'.format(item['url']), path):
                id = item['id']
                pid = item['pid']
                if pid:  #说明是子权限
                    name = item['name'] #有父级显示父级的name
                    request.current_menu_id = pid   #非菜单选项 默认选中
                    request.breadcrumb_list.append({'title': permission[name]['title'], 'url': permission[name]['url']})
                    request.breadcrumb_list.append({'title': item['title'], 'url': item['url']})
                else:    #说明是父权限
                    request.current_menu_id = id
                    request.breadcrumb_list.append({'title': item['title'], 'url': item['url']})
                return
        return HttpResponse('您没有此权限查看此项内容')





