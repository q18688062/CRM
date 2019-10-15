import re
from django.conf import settings
from django.shortcuts import redirect, reverse, HttpResponse
from django.utils.deprecation import MiddlewareMixin



class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        path = request.path_info
        for item in settings.WHITE_LIST:
            if re.match(item, path):
                return

        status = request.session.get(settings.STATUS_KEY)
        if status:
            for item in settings.NO_PERMISSION_LIST:
                if re.match(item, path):
                    return
        else:
            return redirect(reverse('login'))

        permission = request.session.get(settings.PERMISSION_SESSION_KEY)
        for item in permission:
            if re.match(r'{}$'.format(item['url']), path):
                return
        return HttpResponse('您没有此权限查看此项内容')





