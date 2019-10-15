from crm import models
from django.shortcuts import reverse, redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.path_info.startswith('/admin'):
            return None
        if request.path_info in [reverse('login'), reverse('register')]:
            return None
        if not request.session.get('is_login'):
            return redirect(reverse('login'))
        obj_queryset = models.UserProfile.objects.filter(pk=request.session.get('user_id'))
        if obj_queryset:
            request.obj = obj_queryset[0]
