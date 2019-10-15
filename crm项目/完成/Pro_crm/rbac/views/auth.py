
# from rbac import models
# from rbac.service.init_permission import init_permission
# from django.shortcuts import render, redirect, reverse
#
#
# def login(request):
#     error = ''
#     if request.method == 'POST':
#         user = request.POST.get('user')
#         pwd = request.POST.get('pwd')
#         obj = models.User.objects.filter(username=user, password=pwd).first()
#         if obj:
#             init_permission(request, obj)
#             return redirect(reverse('index'))
#         else:
#             error = '账号/密码错误'
#     return render(request, 'login.html', {'error': error})
#
#
#
# def index(request):
#
#     return render(request, 'index.html')


