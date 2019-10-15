from django.conf.urls import url
from crm import views
urlpatterns =[
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^index/', views.index, name='index'),
    url(r'^customer_list/', views.customer, name='customer'),
]