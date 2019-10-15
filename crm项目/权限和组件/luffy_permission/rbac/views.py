from django.shortcuts import render, redirect, reverse
from rbac import models

def login(request):
    error = ''
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        obj = models.User.objects.filter(username=user, password=pwd).first()
        if obj:
            request.session['is_login'] = True
            request.session['role'] = list(obj.roles.filter(permissions__url__isnull=False).values('permissions__url').distinct())
            return redirect(reverse('index'))
        else:
            error = '账号/密码错误'
    return render(request, 'login.html', {'error': error})



def index(request):

    return render(request, 'index.html')