from django import forms
from django.contrib.auth.models import User
from .models import AdminDetail, EmployeeDetail


class ProductKeyForm(forms.ModelForm):
    class Meta:
        model = AdminDetail
        fields = ("product_key",)


class AdminDetailForm(forms.ModelForm):
    class Meta:
        model = AdminDetail
        fields = ["name", "org_name", "phone_number"]


class EmployeeDetailForm(forms.ModelForm):
    class Meta:
        model = EmployeeDetail
        fields = [
            "employee_name",
            "employee_id",
            "phone_number",
            "department",
            "profile_photo",
        ]
