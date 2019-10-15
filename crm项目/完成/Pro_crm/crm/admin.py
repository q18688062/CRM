

from django.contrib import admin

from crm import models


class ConsultantConfig(admin.ModelAdmin):
    list_display = ['id', 'status']

admin.site.register(models.UserProfile)
admin.site.register(models.Department)
admin.site.register(models.Customer)
admin.site.register(models.Campus)
admin.site.register(models.ClassList)
admin.site.register(models.ConsultRecord, ConsultantConfig)
admin.site.register(models.Enrollment)
admin.site.register(models.PaymentRecord)
admin.site.register(models.CourseRecord)
admin.site.register(models.StudyRecord)

