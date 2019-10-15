from crm import models
from django.db import transaction
from crm.views.base import Baseview
from utils.paginator import paginator
from django.conf import settings
from crm.forms import Customer_form, Record_form, Enrollment_form
from django.shortcuts import render, redirect, reverse, HttpResponse


def customer_change(request, pk=None):
    start_obj = models.Customer.objects.filter(pk=pk).first()
    form_obj = Customer_form(instance=start_obj)
    if request.method == 'POST':
        form_obj = Customer_form(data=request.POST, instance=start_obj)
        if form_obj.is_valid():
            form_obj.save()
            next = request.GET.get('next')
            print(next)
            if next:
                return redirect(next)
            return redirect(reverse('customer'))
    title = '编辑客户' if pk else '新建用户'
    return render(request, 'change.html', {'form_obj': form_obj, 'title': title})

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


class CustomerList(Baseview):

    def get(self, request, *args, **kwargs):
        q = self.dispose(['name', 'qq', 'phone', 'source'])
        if request.path_info == reverse('pub_customer'):
            all_customer = models.Customer.objects.filter(q, consultant__isnull=True)
        else:
            all_customer = models.Customer.objects.filter(q, consultant=request.obj)
        res = paginator(request.GET.get('page', 1), all_customer, request.GET.copy(), 5)
        return render(request, 'customer_list.html',
                      {'all_customer': all_customer[res.start_data:res.end_data], 'page': res.page_html})


    def multi_pub(self):

        pk = self.request.POST.getlist('pk')
        if models.Customer.objects.filter(consultant=self.request.obj).count() + len(pk) > settings.MAX_CUSTOMER_NUM:
            return HttpResponse('可领取客户达到上限')
        try:
            with transaction.atomic():
                query_set = models.Customer.objects.filter(pk__in=pk, consultant=None).select_for_update()
                if len(pk) == query_set.count():
                    query_set.update(consultant=self.request.obj)
                else:
                    return HttpResponse('客户已被其他销售领取')
                # self.request.obj.customers.add(*models.Customer.objects.filter(pk__in=pk))
        except Exception as e:
            print(e)


    def multi_apply(self):
        pk = self.request.POST.getlist('pk')

        self.request.obj.customers.remove(*models.Customer.objects.filter(pk__in=pk))


class ConsultList(Baseview):

    def get(self, request, pk=0):
        q = self.dispose(['customer__name', 'consultant__name'])
        if pk:
            all_record = models.ConsultRecord.objects.filter(q, customer_id=pk, delete_status=False)
        else:
            all_record = models.ConsultRecord.objects.filter(q, consultant=request.obj, delete_status=False)
        res = paginator(request.GET.get('page', 1), all_record, request.GET.copy(), 5)
        title = '个人跟进记录' if pk else '跟进记录主页'
        return render(request, 'record_list.html', {'all_record': all_record.order_by('-date')[res.start_data:res.end_data],
                                                'page': res.page_html, 'title': title, 'pk': pk})



def record_change(request, pk=None, customer_id=None):
    start_obj = models.ConsultRecord.objects.filter(pk=pk).first()
    form_obj = Record_form(request, customer_id, instance=start_obj)
    # start_obj = models.ConsultRecord(customer_id=customer_id, consultant=request.obj) if customer_id else models.ConsultRecord.objects.filter(pk=pk).first()
    # form_obj = Record_form(instance=start_obj)
    if request.method == 'POST':
        form_obj = Record_form(request, customer_id, instance=start_obj, data=request.POST)
        # form_obj = Record_form(instance=start_obj, data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('record'))
    title = '修改跟进记录' if pk else '新建跟进记录'
    return render(request, 'change.html', {'form_obj': form_obj, 'title': title})



class EnrollmentList(Baseview):
    def get(self, request, pk=0):
        q = self.dispose(['customer__name', 'school__name'])
        if pk:
            all_enrollment = models.Enrollment.objects.filter(q, customer_id=pk, delete_status=False)
        else:
            all_enrollment = models.Enrollment.objects.filter(q, customer__in=request.obj.customers.all(), delete_status=False)
        res = paginator(request.GET.get('page', 1), all_enrollment, request.GET.copy(), 5)
        title = '个人报名记录' if pk else '报名记录主页'
        return render(request, 'enrollment_list.html', {'all_enrollment': all_enrollment.order_by('-enrolled_date')[res.start_data:res.end_data],
                                                'page': res.page_html, 'title': title, 'pk': pk})



def enrollment_change(request, pk=None, customer_id=None):
    # start_obj = models.Enrollment.objects.filter(pk=pk).first()
    # form_obj = Enrollment_form(request, customer_id, instance=start_obj)
    if customer_id:
        if customer_id == '0':
            start_obj = models.Enrollment(customer_id=0)
            start_obj._user_obj = request.obj
        else:
            start_obj = models.Enrollment(customer_id=customer_id)
    else:
        start_obj = models.Enrollment.objects.filter(pk=pk).first()
    form_obj = Enrollment_form(instance=start_obj)
    if request.method == 'POST':
        # form_obj = Enrollment_form(request, customer_id, instance=start_obj, data=request.POST)
        form_obj = Enrollment_form(instance=start_obj, data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('enrollment'))
    title = '修改报名记录' if pk else '新建报名记录'
    return render(request, 'change.html', {'form_obj': form_obj, 'title': title})