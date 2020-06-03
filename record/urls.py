from django.urls import path
from record.views import profile, employee_list, camera_view, add_employee, att_view


urlpatterns = [
    path("", profile, name="profile"),
    path("employees/", employee_list, name="employee_list"),
    path("add_employee/", add_employee, name="add_employee"),
    path("camera/", camera_view, name="camera_view"),
    path("attendance_details/", att_view, name="att_view"),
]
