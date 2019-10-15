from django.conf.urls import url
from crm import views
urlpatterns =[
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^index/', views.index, name='index'),
    url(r'^customer_list/', views.customer, name='customer'),
    url(r'^add_customer/', views.customer_change, name='add_customer'),
    url(r'^edit_customer/(\d+)/', views.customer_change, name='edit_customer'),
]