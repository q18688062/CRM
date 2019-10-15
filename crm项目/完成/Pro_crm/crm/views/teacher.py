
from crm import models
from utils.paginator import paginator
from crm.views.base import Baseview
from django.shortcuts import render, redirect, reverse
from crm.forms import Class_form, CourseRecord_form, StudyRecord_form



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
        res = paginator(request.GET.get('page', 1), all_course_record, request.GET.copy(), 2)
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
            models.StudyRecord.objects.bulk_create(study_record_list, batch_size=10)



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


# def study_record_list(request, course_record_id=None):
#
#     ModelFormSet =modelformset_factory(models.StudyRecord, StudyRecord_form, extra=0)
#     form_set_obj =ModelFormSet(queryset=models.StudyRecord.objects.filter(course_record_id=course_record_id))
#     if request.method == 'POST':
#         form_set_obj = ModelFormSet(queryset=models.StudyRecord.objects.filter(course_record_id=course_record_id),
#                                     data=request.POST)
#         if form_set_obj.is_valid():
#             form_set_obj.save()
#             next = request.GET.get('next')
#             if next:
#                 return redirect(next)
#             return redirect(reverse('study_record', args=(course_record_id,)))
#     return render(request, 'study_record_list.html', {'form_set_obj': form_set_obj})


def study_record_list(request, course_record_id=None):
    ModelFormSet = modelformset_factory(models.StudyRecord, StudyRecord_form, extra=0)
    form_set_obj = ModelFormSet(queryset=models.StudyRecord.objects.filter(course_record_id=course_record_id))
    if request.method == 'POST':
        form_set_obj = ModelFormSet(queryset=models.StudyRecord.objects.filter(course_record_id=course_record_id),
                                    data=request.POST)
        if form_set_obj.is_valid():
            form_set_obj.save()
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect(reverse('study_record', args=(course_record_id,)))
    return render(request, 'study_record_list.html', {'form_set_obj': form_set_obj})