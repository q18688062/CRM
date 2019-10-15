from django.conf.urls import url
from crm import views
urlpatterns =[
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^customer_list/', views.CustomerList.as_view(), name='customer'),
    url(r'^pub_customer/', views.CustomerList.as_view(), name='pub_customer'),
    url(r'^add_customer/', views.customer_change, name='add_customer'),
    url(r'^edit_customer/(\d+)/', views.customer_change, name='edit_customer'),
    #记录表
    url(r'^record_list/', views.ConsultList.as_view(), name='record'),
    url(r'^add_record/(?P<customer_id>\d+)', views.record_change, name='add_record'),
    url(r'^edit_record/(\d+)/', views.record_change, name='edit_record'),
    url(r'^person_record/(\d+)/', views.ConsultList.as_view(), name='person_record'),
    #报名表
    url(r'^enrollment_list/', views.EnrollmentList.as_view(), name='enrollment'),
    url(r'^add_enrollment/(?P<customer_id>\d+)/', views.enrollment_change, name='add_enrollment'),
    url(r'^edit_enrollment/(\d+)/', views.enrollment_change, name='edit_enrollment'),
    url(r'^person_enrollment/(\d+)/', views.EnrollmentList.as_view(), name='person_enrollment'),
    #班级表
    url(r'^class_list/', views.Classlist.as_view(), name='class'),
    url(r'^add_class/', views.class_change, name='add_class'),
    url(r'^edit_class/(\d+)', views.class_change, name='edit_class'),
    #课程记录
    url(r'^course_record_list/(\d+)', views.CourseRecordList.as_view(), name='course_record_list'),
    url(r'^add_course_record/(?P<class_id>\d+)', views.course_record_change, name='add_course_record'),
    url(r'^edit_course_record/(?P<pk>\d+)', views.course_record_change, name='edit_course_record'),
    #学习记录
    url(r'^study_record/(?P<course_record_id>\d+)', views.study_record_list, name='study_record'),
]

