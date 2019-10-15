import hashlib
from crm import models
from utils.paginator import paginator
from crm.forms import RegForm, Customer_form
from django.shortcuts import render, HttpResponse, redirect, reverse



def login(request):
    if request.session.get('is_login'):
        request.session.flush()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        obj = models.UserProfile.objects.filter(username=username, password=md5.hexdigest(), is_active=True).first()
        if obj:
            request.session['is_login'] = True
            request.session['user_id'] = obj.pk
            return redirect(reverse('customer'))
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误'})
    return render(request, 'login.html')



def register(request):
    form_obj = RegForm()
    if request.method == 'POST':
        form_obj = RegForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('login'))
    return render(request, 'reg.html', {'form_obj': form_obj})



def index(request):
    return HttpResponse('你成功进入')



def customer(request):
    if not request.session.get('is_login'):
        all_customer = models.Customer.objects.filter(consultant_id__isnull=True)
    else:
        all_customer = models.Customer.objects.filter(consultant_id=request.session['user_id'])

    res = paginator(request.GET.get('page', 1), all_customer)
    return render(request, 'customer_list.html', {'all_customer': all_customer[res.start_data:res.end_data], 'page': res.page_html})


# def add_customer(request):
#     form_obj = Customer_form()
#     if request.method == 'POST':
#         form_obj = Customer_form(request.POST)
#         if form_obj.is_valid():
#             form_obj.save()
#             return redirect(reverse('customer'))
#     return render(request, 'add_customer.html', {'form_obj': form_obj})


def customer_change(request, pk=None):
    if request.session.get('is_login'):
        start_obj = models.Customer.objects.filter(pk=pk).first()
        form_obj = Customer_form(instance=start_obj)
        if request.method == 'POST':
            form_obj = Customer_form(data=request.POST,instance=start_obj)
            if form_obj.is_valid():
                form_obj.save()
                return redirect(reverse('customer'))
        title = '编辑客户' if pk else '新建用户'
        return render(request, 'customer_change.html', {'form_obj': form_obj, 'title': title})
    else:
        return redirect(reverse('login'))










