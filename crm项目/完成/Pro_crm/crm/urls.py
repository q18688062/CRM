from django.conf.urls import url
from crm.views import auth, consultant, teacher
urlpatterns =[
    url(r'^login/', auth.login, name='login'),
    url(r'^register/', auth.register, name='register'),
    url(r'^index/', auth.index, name='index'),
    url(r'^customer_list/', consultant.CustomerList.as_view(), name='customer'),
    url(r'^pub_customer/', consultant.CustomerList.as_view(), name='pub_customer'),
    url(r'^add_customer/', consultant.customer_change, name='add_customer'),
    url(r'^edit_customer/(\d+)/$', consultant.customer_change, name='edit_customer'),
    #记录表
    url(r'^record_list/', consultant.ConsultList.as_view(), name='record'),
    url(r'^add_record/(?P<customer_id>\d+)/$', consultant.record_change, name='add_record'),
    url(r'^edit_record/(\d+)/$', consultant.record_change, name='edit_record'),
    url(r'^person_record/(\d+)/$', consultant.ConsultList.as_view(), name='person_record'),
    #报名表
    url(r'^enrollment_list/', consultant.EnrollmentList.as_view(), name='enrollment'),
    url(r'^add_enrollment/(?P<customer_id>\d+)/$', consultant.enrollment_change, name='add_enrollment'),
    url(r'^edit_enrollment/(\d+)/$', consultant.enrollment_change, name='edit_enrollment'),
    url(r'^person_enrollment/(\d+)/$', consultant.EnrollmentList.as_view(), name='person_enrollment'),
    #班级表
    url(r'^class_list/', teacher.Classlist.as_view(), name='class'),
    url(r'^add_class/', teacher.class_change, name='add_class'),
    url(r'^edit_class/(\d+)$', teacher.class_change, name='edit_class'),
    #课程记录
    url(r'^course_record_list/(\d+)$', teacher.CourseRecordList.as_view(), name='course_record_list'),
    url(r'^add_course_record/(?P<class_id>\d+)$', teacher.course_record_change, name='add_course_record'),
    url(r'^edit_course_record/(?P<pk>\d+)$', teacher.course_record_change, name='edit_course_record'),
    #学习记录
    url(r'^study_record/(?P<course_record_id>\d+)$', teacher.study_record_list, name='study_record'),
]

