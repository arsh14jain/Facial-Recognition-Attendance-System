from django.contrib import admin
from .models import Product, AdminDetail, EmployeeDetail, Attendance

# Register your models here.
admin.site.register(Product)
admin.site.register(AdminDetail)
admin.site.register(EmployeeDetail)
admin.site.register(Attendance)
