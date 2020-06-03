from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime


class Product(models.Model):
    product_key = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.product_key


class AdminDetail(models.Model):
    product_key = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, related_name="admindetail"
    )
    name = models.CharField(max_length=200, null=True, default="")
    org_name = models.CharField(max_length=200, null=True, default="")
    phone_number = models.CharField(max_length=10, null=True, default="")


class EmployeeDetail(models.Model):
    product_key = models.ForeignKey(Product, on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=200)
    employee_id = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10, null=True, default="")
    department = models.CharField(max_length=200)
    profile_photo = models.ImageField(upload_to="images/", null=True)

    def __str__(self):
        return self.employee_id


class Attendance(models.Model):
    product_key = models.ForeignKey(Product, on_delete=models.CASCADE)
    attendance_date = models.DateField(default=datetime.date.today)
    employeeid = models.ForeignKey(EmployeeDetail, on_delete=models.CASCADE)
