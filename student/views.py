# student/views.py
from django.shortcuts import render
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,redirect, render)
from .models import *
from faculty.models import *
from course.models import *
from attendance.models import *
import math
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from django.http import HttpResponse, JsonResponse
from .forms import *
from django.contrib import messages
from django.urls import reverse
from django.core.files.storage import FileSystemStorage

from django.contrib.auth.decorators import login_required


def student_home(request):
    student = get_object_or_404(Student,admin = request.user)
    print(f'requested user is {request.user}')                                   # Print
    print(Student.objects.filter(admin=request.user).exists())                     #Print 2
    total_subject = Subject.objects.filter(course = student.course).count()
    total_attendance = AttendanceReport.objects.filter(student=student).count()
    total_present = AttendanceReport.objects.filter(student=student,status = True).count()

    if total_attendance==0:
         percent_absent = percent_present = 0
    else:
        percent_present = math.floor((total_present/total_attendance)*100)
        percent_absent = math.ceil(100-percent_present)

    subject_name = []
    data_present = []
    data_absent = []

    subjects = Subject.objects.filter(course = student.course)
    for subject in subjects:
        # attendance = Attendance.objects.filter(subject=subject)
        # present_count = AttendanceReport.objects.filter(attendance_in = attendance, status = True, student= student).count()
        # absent_count = AttendanceReport.objects.filter(attendance_in = attendance,status = False,student = student).count()

        subject_name.append(subject.name)
        # data_present.append(present_count)
        # data_absent.append(absent_count)


    context = {
        'total_attendance': total_attendance,
        'percent_present': percent_present,
        'percent_absent': percent_absent,
        'total_subject': total_subject,
        'subjects': subjects,
        'data_present': data_present,
        'data_absent': data_absent,
        'data_name': subject_name,
        'page_title': str(student.admin.first_name)+" " +str(student.admin.last_name)

    }

    return  render(request,'student/home.html',context)


# @csrf_exempt
# def student_view_attendance(request):
#     student = get_object_or_404(Student, admin=request.user)
    
#     if request.method != 'POST':
#         course = get_object_or_404(Course, id=student.course.id)
#         context = {
#             'subjects': Subject.objects.filter(course=course),
#             'page_title': 'View Attendance'
#         }
#         return render(request, 'student/attendance_view.html', context)
#     else:
#         subject_id = request.POST.get('subject')
#         start_date_str = request.POST.get('start_date')
#         end_date_str = request.POST.get('end_date')

#         try:
#             subject = get_object_or_404(Subject, id=subject_id)
#             start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
#             end_date = datetime.strptime(end_date_str, "%d-%m-%Y")

#             attendance = Attendance.objects.filter(date__range=(start_date, end_date), subject=subject)
#             attendance_reports = AttendanceReport.objects.filter(attendance__in=attendance, student=student)

#             json_data = []
#             for report in attendance_reports:
#                 data = {
#                     "date": report.attendance.date.strftime("%d-%m-%Y"),
#                     "status": report.status
#                 }
#                 json_data.append(data)

#             return JsonResponse(json.dumps(json_data), safe=False)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def student_view_attendance(request):
    student = get_object_or_404(Student, admin=request.user)

    if request.method != 'POST':
        course = get_object_or_404(Course, id=student.course.id)
        context = {
            'subjects': Subject.objects.filter(course=course),
            'page_title': 'View Attendance'
        }
        return render(request, 'student/attendance_view.html', context)
    else:
        subject_id = request.POST.get('subject')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        try:
            subject = get_object_or_404(Subject, id=subject_id)
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

            # Fetch attendance within the date range for the given subject
            attendance = Attendance.objects.filter(date__range=(start_date, end_date), subject=subject)
            attendance_reports = AttendanceReport.objects.filter(attendance__in=attendance, student=student)

            # Calculate percentages
            total_attendance = attendance_reports.count()
            present_count = attendance_reports.filter(status=True).count()  # True for Present
            absent_count = attendance_reports.filter(status=False).count()   # False for Absent

            percent_present = (present_count / total_attendance * 100) if total_attendance > 0 else 0
            percent_absent = (absent_count / total_attendance * 100) if total_attendance > 0 else 0

            # Prepare JSON data for response
            json_data = {
                'attendance': [],
                'percent_present': percent_present,
                'percent_absent': percent_absent
            }
            for report in attendance_reports:
                data = {
                    "date": report.attendance.date.strftime("%Y-%m-%d"),
                    "status": 'Present' if report.status else 'Absent'  # Convert True/False to Present/Absent
                }
                json_data['attendance'].append(data)

            return JsonResponse(json_data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)



# def student_apply_leave(request):
#     form = LeaveReportStudentForm(request.POST or None)
#     student = get_object_or_404(Student,admin_id =request.user.id)
#     context={
#         'form': form,
#         'leave_history': LeaveReportStudent.objects.filter(student=student),
#         'page_title': 'Apply for leave'
#     }
#     if request.method =='POST':
#         if form.is_valid():
#             try:
#                 obj = form.save(commit= False)
#                 obj.student = student
#                 obj.save()
#                 messages.success(
#                     request, "Application for leave has been submitted for review")
#                 return redirect(reverse('student_apply_leave'))
#             except Exception:
#                 messages.error(request, "Could not submit")
#         else:
#             messages.error(request, "Form has errors!")
#     return render(request,'student/apply_leave.html',context)

def student_apply_leave(request):
    student = get_object_or_404(Student, admin_id=request.user.id)
    form = LeaveReportStudentForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            try:
                leave_report = form.save(commit=False)
                leave_report.student = student  # Assign the student to the leave report
                leave_report.save()
                messages.success(request, "Application for leave has been submitted for review.")
                return redirect('student:student_apply_leave')  # Make sure this matches your URL pattern
            except Exception as e:
                messages.error(request, f"Could not submit: {str(e)}")
        else:
            messages.error(request, "Form has errors!")

    # Retrieve leave history for the student
    leave_history = LeaveReportStudent.objects.filter(student=student)
    for leave in leave_history:
        print(leave.date)

    context = {
        'form': form,
        'leave_history': leave_history,
        'page_title': 'Apply for Leave',
    }

    return render(request, 'student/apply_leave.html', context)


def student_feedback(request):
    form = FeedbackStudentForm(request.POST or None)
    student = get_object_or_404(Student, admin_id=request.user.id)
    context = {
        'form': form,
        'feedbacks': FeedbackStudent.objects.filter(student=student),
        'page_title': 'Student Feedback'

    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.student = student
                obj.save()
                messages.success(
                    request, "Feedback submitted for review")
                return redirect(reverse('student_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request,'student/feedback.html',context)

def student_view_profile(request):
    student = get_object_or_404(Student, admin=request.user)
    form = StudentEditForm(request.POST or None, request.FILES or None,
                           instance=student)
    context = {'form': form,
               'page_title': 'View/Edit Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                passport = request.FILES.get('profile_pic') or None
                admin = student.admin
                if password != None:
                    admin.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    admin.profile_pic = passport_url
                admin.first_name = first_name
                admin.last_name = last_name
                admin.address = address
                admin.gender = gender
                admin.save()
                student.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('student_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(request, "Error Occured While Updating Profile " + str(e))
    return render(request,'student/view_profile.html',context)


@csrf_exempt
def student_fcmtoken(request):
    token = request.POST.get('token')
    student_user = get_object_or_404(CustomUser, id=request.user.id)
    try:
        student_user.fcm_token = token
        student_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")

def student_view_notification(request):
    student = get_object_or_404(Student, admin=request.user)
    notifications = NotificationStudent.objects.filter(student=student)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request,'student/view_notification.html',context)

def student_view_result(request):
    student = get_object_or_404(Student, admin=request.user)
    results = StudentResult.objects.filter(student=student)
    context = {
        'results': results,
        'page_title': "View Results"
    }
    return render(request,'student/view_result.html',context)