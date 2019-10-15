import hashlib
from crm import models
from django.views import View
from crm.view.base import Baseview
from utils.paginator import paginator
from django.db import transaction
from django.conf import global_settings, settings
from django.shortcuts import render, redirect, reverse, HttpResponse
from crm.forms import RegForm, Customer_form, Record_form, Enrollment_form, Class_form, CourseRecord_form, StudyRecord_form





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
        q = self.dispose(['name', 'qq', 'phone'])
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




# def record_list(request, pk=None):
#     if pk:
#         all_record = models.ConsultRecord.objects.filter(customer_id=pk)
#     else:
#         all_record = models.ConsultRecord.objects.filter(consultant=request.obj)
#     title = '个人跟进记录' if pk else '跟进记录主页'
#     res = paginator(request.GET.get('page', 1), all_record, request.GET.copy(), 5)
#     return render(request, 'record_list.html', {'all_record': all_record[res.start_data:res.end_data],
#                                                 'page': res.page_html, 'title': title})


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
    if request.method == 'POST':
        form_obj = Record_form(request, customer_id, instance=start_obj, data=request.POST)
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


class Classlist(Baseview):

    def get(self, request):
        q = self.dispose(['campuses__name', 'start_date'])
        all_class = models.ClassList.objects.filter(q)
        res = paginator(request.GET.get('page', 1), all_class, request.GET.copy(), 5)
        return render(request, 'class_list.html',
                      {'all_class': all_class[res.start_data:res.end_data], 'page': res.page_html})



def class_change(request,pk=None):
    start_obj = models.ClassList.objects.filter(pk=pk).first()
    form_obj = Class_form(instance=start_obj)
    if request.method == 'POST':
        form_obj = Class_form(data=request.POST, instance=start_obj)
        if form_obj.is_valid():
            form_obj.save()
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect(reverse('class'))
    title = '编辑班级' if pk else '新建班级'
    return render(request, 'change.html', {'form_obj': form_obj, 'title': title})


class CourseRecordList(Baseview):
    def get(self, request, class_id):
        q = self.dispose(['course_title', 'homework_title', 'teacher__name'])
        all_course_record = models.CourseRecord.objects.filter(q, re_class_id=class_id)
        res = paginator(request.GET.get('page', 1), all_course_record, request.GET.copy(), 5)
        return render(request, 'course_record_list.html',
                      {'all_course_record': all_course_record[res.start_data:res.end_data], 'page': res.page_html, 'class_id': class_id})

    def multi_init(self):
        course_record_id_list = self.request.POST.getlist('pk')
        course_record = models.CourseRecord.objects.filter(pk__in=course_record_id_list)
        for one_course_record in course_record:
            all_student = one_course_record.re_class.customer_set.all().filter(status='studying')
            study_record_list = []
            for student in all_student:
                study_record_list.append(models.StudyRecord(student=student, course_record=one_course_record))
            models.StudyRecord.objects.bulk_create(study_record_list)




def course_record_change(request, pk=None, class_id=None):
    start_obj = models.CourseRecord(re_class_id=class_id, recorder=request.obj) if class_id else models.CourseRecord.objects.filter(pk=pk).first()
    form_obj = CourseRecord_form(instance=start_obj)
    if request.method == 'POST':
        form_obj = CourseRecord_form(data=request.POST, instance=start_obj)
        if form_obj.is_valid():
            form_obj.save()
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect(reverse('course_record_list', args=(class_id,)))
    title = '编辑课程记录' if pk else '新建课程记录'
    return render(request, 'change.html', {'form_obj': form_obj, 'title': title})


from django.forms import modelformset_factory


def study_record_list(request, course_record_id=None):

    ModelFormSet =modelformset_factory(models.StudyRecord, StudyRecord_form, extra=0)
    form_set_obj =ModelFormSet(queryset=models.StudyRecord.objects.filter(course_record_id=course_record_id))
    if request.method == 'POST':
        form_set_obj = ModelFormSet(queryset=models.StudyRecord.objects.filter(course_record_id=course_record_id),
                                    data=request.POST)
        if form_set_obj.is_valid():
            form_set_obj.save()
            next = request.GET.get('next')
            print(next)
            if next:
                return redirect(next)
            return redirect(reverse('study_record', args=(course_record_id,)))
    return render(request, 'study_record_list.html', {'form_set_obj': form_set_obj})





