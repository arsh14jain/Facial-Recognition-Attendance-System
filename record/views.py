from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
import face_recognition
from .forms import ProductKeyForm, AdminDetailForm, EmployeeDetailForm
from django.views.decorators.csrf import csrf_exempt
from .models import EmployeeDetail, Attendance
from django.http import JsonResponse
import xlsxwriter
from datetime import date
import numpy
import base64
import io

# Create your views here.
@login_required
def profile(request):
    uname = request.user.admindetail.name
    return render(request, "profile/profile.html",{"name": uname})


def signup(request):

    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        admin_form = ProductKeyForm(request.POST)
        if user_form.is_valid():
            if admin_form.is_valid():
                user_form.save()
                username = user_form.cleaned_data.get("username")
                password = user_form.cleaned_data.get("password1")
                user = authenticate(username=username, password=password)
                ad = admin_form.save(commit=False)
                ad.user = user
                ad.save()
                new_user = authenticate(
                    username=user_form.cleaned_data["username"],
                    password=user_form.cleaned_data["password1"],
                )
                login(request, new_user)
                request = "GET"
                return redirect("/accounts/admin_details/")

    user_form = UserCreationForm()
    admin_form = ProductKeyForm()
    return render(
        request,
        "registration/signup.html",
        {"user_form": user_form, "admin_form": admin_form,},
    )


@login_required
def admin_details(request):
    if request.method == "POST":
        form = AdminDetailForm(data=request.POST, instance=request.user.admindetail)
        # print(form["name"].value())
        if form.is_valid():
            form.save()
            request = "GET"
            return redirect("/")
    else:
        form = AdminDetailForm()
        return render(request, "registration/admin_details.html", {"form": form})


@login_required
def employee_list(request):
    emps = []
    emps = EmployeeDetail.objects.filter(
        product_key=request.user.admindetail.product_key
    )
    print(emps)
    return render(request, "profile/employees.html", {"emps": emps})


@login_required
@csrf_exempt
def camera_view(request):
    if request.method == "POST":
        img11 = request.POST.get("mydata")
        # img = request.FILES["webcam"]
        imgdata = base64.b64decode(img11)
        filename = "some_image.jpg"
        with open(filename, "wb") as f:
            f.write(imgdata)
        # print(img11)
        image1 = face_recognition.load_image_file(filename)
        face_encoding1 = face_recognition.face_encodings(image1)[0]
        emps = EmployeeDetail.objects.all()
        nm = "Not Found"
        for emp in emps:
            image2 = face_recognition.load_image_file(emp.profile_photo)
            face_encoding2 = face_recognition.face_encodings(image2)[0]
            results = face_recognition.compare_faces([face_encoding1], face_encoding2)
            print(emp.employee_name)
            print(results)
            if results[0]:
                nm = emp.employee_name
                empid = emp.employee_id
                break

        a = Attendance(
            product_key=request.user.admindetail.product_key,
            employeeid=EmployeeDetail.objects.get(
                employee_id=empid, product_key=request.user.admindetail.product_key
            ),
        )
        a.save()
        return render(request, "camera/result.html",{"name":nm})
    else:
        return render(request, "camera/cam.html")


@login_required
def add_employee(request):
    if request.method == "POST":
        product_ke = request.user.admindetail.product_key
        emp_form = EmployeeDetailForm(request.POST, request.FILES)
        if emp_form.is_valid():
            # product_key = request.user.admindetail.product_key
            e = emp_form.save(commit=False)
            e.product_key = product_ke
            e.save()
            return HttpResponse("Employee Added!!")
        return HttpResponse("Invalid Form")
    form = EmployeeDetailForm()
    return render(request, "registration/add_employee.html", {"form": form})


@login_required
def att_view(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    cell_format = workbook.add_format()
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({"bold": True})
    worksheet.write("A1", "Employees present today", bold)
    worksheet.write("A3", "Name", bold)
    worksheet.write("B3", "ID", bold)
    p = Attendance.objects.filter(
        product_key=request.user.admindetail.product_key, attendance_date=date.today(),
    )
    row = 4
    col = 0
    for present in p:
        name = EmployeeDetail.objects.filter(
            product_key=request.user.admindetail.product_key,
            employee_id=present.employeeid,
        )[0].employee_name
        worksheet.write(row, col, name)
        id = "" + str(present.employeeid)
        # id = present.employeeid
        worksheet.write(row, col + 1, id)
        row += 1

    print("here")
    print(p)
    print("here")
    workbook.close()
    output.seek(0)
    filename = "report.xlsx"
    response = HttpResponse(
        output,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = "attachment; filename=%s" % filename

    return response
