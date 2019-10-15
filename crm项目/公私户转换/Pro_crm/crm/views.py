import hashlib
from crm import models
from django.views import View
from django.db.models import Q
from utils.paginator import paginator
from crm.forms import RegForm, Customer_form
from django.shortcuts import render, redirect, reverse




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


# def add_customer(request):
#     form_obj = Customer_form()
#     if request.method == 'POST':
#         form_obj = Customer_form(request.POST)
#         if form_obj.is_valid():
#             form_obj.save()
#             return redirect(reverse('customer'))
#     return render(request, 'add_customer.html', {'form_obj': form_obj})


def customer_change(request, pk=None):
    start_obj = models.Customer.objects.filter(pk=pk).first()
    form_obj = Customer_form(instance=start_obj)
    if request.method == 'POST':
        form_obj = Customer_form(data=request.POST, instance=start_obj)
        if form_obj.is_valid():
            form_obj.save()
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect(reverse('customer'))
    title = '编辑客户' if pk else '新建用户'
    return render(request, 'customer_change.html', {'form_obj': form_obj, 'title': title})



# def customer_batch(request):
#     batch_obj = request.POST.get('operation')
#     for key in request.POST:
#         if key == 'csrfmiddlewaretoken' or key == 'operation':
#             continue
#         if batch_obj == 'gs':
#             request.obj.customers.add(*models.Customer.objects.filter(pk=key))
#         else:
#             request.obj.customers.remove(*models.Customer.objects.filter(pk=key))
#     return redirect(reverse('customer'))
#
#
# def customer(request):
#     find_obj = request.GET.get('content')
#     if find_obj:
#         if request.path_info == reverse('pub_customer'):
#             all_customer = models.Customer.objects.filter(
#                 Q(qq__contains=find_obj) | Q(name__contains=find_obj) | Q(phone__contains=find_obj),
#                 consultant_id__isnull=True)
#         else:
#             all_customer = models.Customer.objects.filter(
#                 Q(qq__contains=find_obj) | Q(name__contains=find_obj) | Q(phone__contains=find_obj),
#                 consultant=request.obj)
#     else:
#         if request.path_info == reverse('pub_customer'):
#             all_customer = models.Customer.objects.filter(consultant_id__isnull=True)
#         else:
#             all_customer = models.Customer.objects.filter(consultant_id=request.obj.pk)
#     res = paginator(request.GET.get('page', 1), all_customer)
#     return render(request, 'customer_list.html', {'all_customer': all_customer[res.start_data:res.end_data], 'page': res.page_html})


class CustomerList(View):

    def get(self, request, *args, **kwargs):
        q = self.dispose(['name', 'qq', 'phone'])
        if request.path_info == reverse('pub_customer'):
            all_customer = models.Customer.objects.filter(q, consultant__isnull=True)
        else:
            all_customer = models.Customer.objects.filter(q, consultant=request.obj)
        res = paginator(request.GET.get('page', 1), all_customer, request.GET.copy(), 2)
        return render(request, 'customer_list.html',
                      {'all_customer': all_customer[res.start_data:res.end_data], 'page': res.page_html})



    def post(self, request, *args, **kwargs):
        operation = request.POST.get('operation')
        print(operation)
        if hasattr(self, operation):
            getattr(self, operation)()
            return self.get(request, *args, **kwargs)


    def multi_pub(self):
        pk = self.request.POST.getlist('pk')
        self.request.obj.customers.add(*models.Customer.objects.filter(pk__in=pk))


    def multi_apply(self):
        pk = self.request.POST.getlist('pk')
        self.request.obj.customers.remove(*models.Customer.objects.filter(pk__in=pk))

    def dispose(self, field_list):
        content = self.request.GET.get('content', '')
        q = Q()
        q.connector = 'OR'
        for field in field_list:
            q.children.append(Q(('{}__contains'.format(field), content)))
        return q











