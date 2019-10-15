import hashlib
from crm import models
from utils.paginator import paginator
from crm.forms import RegForm,Logform
from django.shortcuts import render,HttpResponse,redirect,reverse



def login(request):
    form_obj = Logform()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        obj = models.UserProfile.objects.filter(username=username, password=md5.hexdigest(), is_active=True).first()
        if obj:
            return redirect(reverse('index'))
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误'})
    return render(request, 'login.html', {'form_obj': form_obj})



def register(request):
    form_obj = RegForm()
    if request.method == 'POST':
        form_obj = RegForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('login'))
    return render(request, 'login.html', {'form_obj': form_obj})



def index(request):
    return HttpResponse('你成功进入')



def customer(request):
    all_customer = models.Customer.objects.all()
    res = paginator(request.GET.get('page', 1), all_customer, 2)
    return render(request, 'customer_list.html', {'all_customer': all_customer[res.start_data:res.end_data], 'page': res.page_html})

