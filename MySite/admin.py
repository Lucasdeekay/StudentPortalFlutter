from django.contrib import admin

from MySite.models import Student, CourseMaterial, Notification, PaymentRecord


# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "matric_no", "email", "program", "level", "enrollment_date")


class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "upload_date", "program")


class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "content", "time")


class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = ("student", "amount", "method", "transaction_id", "time")


admin.site.register(Student, StudentAdmin)
admin.site.register(CourseMaterial, CourseMaterialAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(PaymentRecord, PaymentRecordAdmin)
