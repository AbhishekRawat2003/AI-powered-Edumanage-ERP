from django.shortcuts import (HttpResponseRedirect, get_object_or_404,redirect, render)
from .models import *
from .forms import *
from student.models import *
from course.models import *
from attendance.models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from student.forms import *
from course.forms import *
import requests
from django.views import View

@login_required
def faculty_home(request):
    faculty = get_object_or_404(Faculty,admin=request.user)
    print(f'requested user is {request.user}')                                   # Print
    print(Faculty.objects.filter(admin=request.user).exists())
    total_students = Student.objects.filter(course=faculty.course).count()
    total_leave = LeaveReportFaculty.objects.filter(faculty=faculty).count()
    subjects = Subject.objects.filter(faculty=faculty)
    total_subject = subjects.count()
    attendance_list = Attendance.objects.filter(subject__in=subjects)
    total_attendance = attendance_list.count()
    attendance_list = []
    subject_list = []
    for subject in subjects:
        attendance_count = Attendance.objects.filter(subject=subject).count()
        subject_list.append(subject.name)
        attendance_list.append(attendance_count)
    context = {
        'page_title': 'Faculty Panel - ' + str(faculty.admin.first_name) + " "+str(faculty.admin.last_name) + " "+ ' (' + str(faculty.course) + ')',
        'total_students': total_students,
        'total_attendance': total_attendance,
        'total_leave': total_leave,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list
    }
    return render(request,'faculty/home.html',context)


def faculty_take_attendance(request):
    faculty = get_object_or_404(Faculty,admin = request.user)
    subjects = Subject.objects.filter(faculty_id = faculty)
    sessions = Session.objects.all()
    for session in sessions:
        print(session.end_year.year)
    context = {
        'subjects': subjects,
        'sessions': sessions,
        'page_title': 'Take Attendance'
    }
    return render(request,'faculty/take_attendance.html',context)

@csrf_exempt
def get_students(request):
    subject_id = request.POST.get('subject')
    session_id =request.POST.get('session')
    try:
        subject = get_object_or_404(Subject, id=subject_id)
        session = get_object_or_404(Session, id=session_id)
        students = Student.objects.filter(
            course_id=subject.course.id, session=session)
        student_data = []
        print(f"Subject ID: {subject_id}, Session ID: {session_id}")
        for student in students:
            data = {
                    "id": student.id,
                    "name": student.admin.last_name + " " + student.admin.first_name
                    }
            student_data.append(data)
        return JsonResponse(json.dumps(student_data), content_type='application/json', safe=False)
    except Exception as e:
        return e


# @csrf_exempt
# def save_attendance(request):
#     student_data = request.POST.get('student_ids')
#     date = request.POST.get('date')
#     subject_id = request.POST.get('subject')
#     session_id = request.POST.get('session')
#     students = json.loads(student_data)
#     try:
#         session = get_object_or_404(Session, id=session_id)
#         subject = get_object_or_404(Subject, id=subject_id)
#         attendance, created = Attendance.objects.get_or_create(session=session, subject=subject, date=date)

#         for student_dict in students:
#             student = get_object_or_404(Student, id=student_dict.get('id'))

#             attendance_report, report_created = AttendanceReport.objects.get_or_create(student=student, attendance=attendance)

#             # Update the status only if the attendance report was newly created
#             if report_created:
#                 attendance_report.status = student_dict.get('status')
#                 attendance_report.save()

#     except Exception as e:
#         print("Error saving attendance:", e)  # or use logging
#         return HttpResponse("Failed to save attendance", status=500)

#     return HttpResponse("OK")


@csrf_exempt
def save_attendance(request):
    if request.method == 'POST':
        student_data = request.POST.get('student_ids')
        date = request.POST.get('date')
        subject_id = request.POST.get('subject')
        session_id = request.POST.get('session')

        try:
            # Log the input data for debugging
            print(f"Student Data: {student_data}, Date: {date}, Subject ID: {subject_id}, Session ID: {session_id}")

            # Parse JSON data
            students = json.loads(student_data)

            # Fetch session and subject
            session = get_object_or_404(Session, id=session_id)
            subject = get_object_or_404(Subject, id=subject_id)

            # Get or create the attendance record
            attendance, created = Attendance.objects.get_or_create(session=session, subject=subject, date=date)

            for student_dict in students:
                student = get_object_or_404(Student, id=student_dict.get('id'))

                # Get or create the attendance report
                attendance_report, report_created = AttendanceReport.objects.get_or_create(student=student, attendance=attendance)

                # Convert status to Boolean
                status_value = student_dict.get('status')
                attendance_report.status = True if status_value == "Present" else False  # Ensure status is boolean
                attendance_report.save()

            print("Attendance saved successfully.")
            return JsonResponse({"status": "success", "message": "Attendance saved successfully."})

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format."}, status=400)
        except Exception as e:
            print("Error saving attendance:", e)  # Log error with traceback for more context
            return JsonResponse({"status": "error", "message": "Failed to save attendance."}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)




def faculty_update_attendance(request):
    faculty = get_object_or_404(faculty,admin= request.user)
    subjects = Subject.objects.filter(faculty_id= faculty)
    sessions = sessions.objects.all()
    context = {
        'subjects': subjects,
        'sessions': sessions,
        'page_title': 'Update Attendance'
    }

    return render(request,'faculty/update_attendance.html',context)

@csrf_exempt
def get_student_attendance(request):
    attendance_date_id = request.POST.get('attendance_date_id')
    try:
        date = get_object_or_404(Attendance, id=attendance_date_id)
        attendance_data = AttendanceReport.objects.filter(attendance=date)
        student_data = []
        for attendance in attendance_data:
            data = {"id": attendance.student.admin.id,
                    "name": attendance.student.admin.last_name + " " + attendance.student.admin.first_name,
                    "status": attendance.status}
            student_data.append(data)
        return JsonResponse(json.dumps(student_data), content_type='application/json', safe=False)
    except Exception as e:
        return e


@csrf_exempt
def update_attendance(request):
    student_data = request.POST.get('student_ids')
    date = request.POST.get('date')
    students = json.loads(student_data)
    try:
        attendance = get_object_or_404(Attendance, id=date)

        for student_dict in students:
            student = get_object_or_404(
                Student, admin_id=student_dict.get('id'))
            attendance_report = get_object_or_404(AttendanceReport, student=student, attendance=attendance)
            attendance_report.status = student_dict.get('status')
            attendance_report.save()
    except Exception as e:
        return None

    return HttpResponse("OK")

def faculty_apply_leave(request):
    form = LeaveReportFacultyForm(request.POST or None)
    faculty = get_object_or_404(Faculty,admin_id=request.user.id)
    context={
        form : form,
        'leave_history': LeaveReportFaculty.objects.filter(faculty=faculty),
        'page_title': 'Apply for Leave'
        }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.faculty = faculty
                obj.save()
                messages.success(
                    request, "Application for leave has been submitted for review")
                return redirect(reverse('faculty_apply_leave'))
            except Exception:
                messages.error(request, "Could not apply!")
        else:
            messages.error(request, "Form has errors!")
            
    return render(request,'faculty/apply_leave.html',context)

def faculty_feedback(request):
    form = FeedbackFacultyForm(request.POST or None)
    faculty =  get_object_or_404(Faculty,admin_id = request.user.id)
    context = {
        'form': form,
        'feedbacks': FeedbackFaculty.objects.filter(faculty=faculty),
        'page_title': 'Add Feedback'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.faculty = faculty
                obj.save()
                messages.success(request, "Feedback submitted for review")
                return redirect(reverse('faculty_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
            
    return render(request,'faculty/feedback.html',context)

# @login_required
# def faculty_view_profile(request):
#     faculty = get_object_or_404(Faculty, admin=request.user)
#     form = FacultyEditForm(request.POST or None, request.FILES or None,instance=faculty)
#     context = {'form': form,
#                'page_title': 'View/Update Profile',
#                 }
#     if request.method == 'POST':
#         try:
#             if form.is_valid():
#                 first_name = form.cleaned_data.get('first_name')
#                 last_name = form.cleaned_data.get('last_name')
#                 password = form.cleaned_data.get('password') or None
#                 address = form.cleaned_data.get('address')
#                 gender = form.cleaned_data.get('gender')
#                 # passport = request.FILES.get('profile_pic') or None
#                 passport = request.FILES.get('profile_pic') or None
#                 admin = faculty.admin
#                 if password != None:
#                     admin.set_password(password)
#                 if passport != None:
#                     fs = FileSystemStorage()
#                     filename = fs.save(passport.name, passport)
#                     passport_url = fs.url(filename)
#                     print("Uploaded profile picture URL:", passport_url)
#                     admin.profile_pic = passport_url
#                 admin.first_name = first_name
#                 admin.last_name = last_name
#                 admin.address = address
#                 admin.gender = gender
#                 admin.save()
#                 faculty.save()
#                 messages.success(request, "Profile Updated!")
#                 return redirect(reverse('faculty_view_profile'))
#             else:
#                 messages.error(request, "Invalid Data Provided")
#                 return render(request,'faculty/view_profile.html',context)
#         except Exception as e:
#             messages.error(
#                 request, "Error Occured While Updating Profile " + str(e))
#             return render(request,'faculty/view_profile.html',context)

#     return render(request,'faculty/view_profile.html',context)


@login_required
def faculty_view_profile(request):
    faculty = get_object_or_404(Faculty, admin=request.user)
    form = FacultyEditForm(request.POST or None, request.FILES or None, instance=faculty)
    
    if request.method == 'POST':
        if form.is_valid():
            # Your processing logic
            passport = request.FILES.get('profile_pic')  # This should get the uploaded file
            if passport:
                faculty.admin.profile_pic = passport  # Assign the uploaded file to the admin's profile_pic field
            # Other form processing
            faculty.admin.save()  # Save the changes to the admin user
            faculty.save()  # Save any changes to the faculty model
            messages.success(request, "Profile Updated!")
            return redirect('faculty_view_profile')
        else:
            messages.error(request, "Invalid Data Provided")
            print(form.errors)  # Print form errors for debugging
    
    context = {
        'form': form,
        'page_title': 'View/Update Profile',
        'faculty': faculty,
    }
    return render(request, 'faculty/view_profile.html', context)



@csrf_exempt
def faculty_fcmtoken(request):
    token = request.POST.get('token')
    try:
        faculty_user = get_object_or_404(CustomUser, id=request.user.id)
        faculty_user.fcm_token = token
        faculty_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")

def faculty_view_notification(request):
    faculty = get_object_or_404(Faculty, admin=request.user)
    notifications = NotificationFaculty.objects.filter(faculty=faculty)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request,'faculty/view_notification.html',context)

# def faculty_add_result(request):
#     faculty = get_object_or_404(Faculty, admin=request.user)
#     subjects = Subject.objects.filter(faculty=faculty)
#     sessions = Session.objects.all()
#     context = {
#         'page_title': 'Result Upload',
#         'subjects': subjects,
#         'sessions': sessions
#     }
#     if request.method == 'POST':
#         try:
#             student_id = request.POST.get('student_list')
#             subject_id = request.POST.get('subject')
#             test = request.POST.get('test')
#             exam = request.POST.get('exam')
#             student = get_object_or_404(Student, id=student_id)
#             subject = get_object_or_404(Subject, id=subject_id)
#             try:
#                 data = StudentResult.objects.get(
#                     student=student, subject=subject)
#                 data.exam = exam
#                 data.test = test
#                 data.save()
#                 messages.success(request, "Scores Updated")
#             except:
#                 result = StudentResult(student=student, subject=subject, test=test, exam=exam)
#                 result.save()
#                 messages.success(request, "Scores Saved")
#         except Exception as e:
#             messages.warning(request, "Error Occured While Processing Form")
#     return render(request, "faculty/add_result.html", context)


# @csrf_exempt
# def fetch_student_result(request):
#     try:
#         subject_id = request.POST.get('subject')
#         student_id = request.POST.get('student')
#         student = get_object_or_404(Student, id=student_id)
#         subject = get_object_or_404(Subject, id=subject_id)
#         result = StudentResult.objects.get(student=student, subject=subject)
#         result_data = {
#             'exam': result.exam,
#             'test': result.test
#         }
#         return HttpResponse(json.dumps(result_data))
#     except Exception as e:
#         return HttpResponse('False')



def faculty_add_result(request):
    faculty = get_object_or_404(Faculty, admin=request.user)
    subjects = Subject.objects.filter(faculty=faculty)
    sessions = Session.objects.all()
    
    # Debugging: Check if subjects are being fetched correctly
    print(f"Subjects: {[subject.name for subject in subjects]}")
    
    # Fetch students for the faculty
    students = Student.objects.all()  # Fetch all students or filter based on faculty
    print(f"Students: {[student.admin.first_name + ' ' + student.admin.last_name for student in students]}")  # Log student names

    context = {
        'page_title': 'Result Upload',
        'subjects': subjects,
        'sessions': sessions,
        'students': students  # Pass students to the context
    }
    
    if request.method == 'POST':
        try:
            student_id = request.POST.get('student_list')
            subject_id = request.POST.get('subject')
            test = request.POST.get('test')
            exam = request.POST.get('exam')
            student = get_object_or_404(Student, id=student_id)
            subject = get_object_or_404(Subject, id=subject_id)

            # Debugging: Print the received values
            print(f"Received - Student ID: {student_id}, Subject ID: {subject_id}, Test: {test}, Exam: {exam}")

            try:
                data = StudentResult.objects.get(student=student, subject=subject)
                data.exam = exam
                data.test = test
                data.save()
                messages.success(request, "Scores Updated")
            except StudentResult.DoesNotExist:
                result = StudentResult(student=student, subject=subject, test=test, exam=exam)
                result.save()
                messages.success(request, "Scores Saved")
        except Exception as e:
            messages.warning(request, f"Error Occurred While Processing Form: {str(e)}")
    
    return render(request, "faculty/add_result.html", context)

@csrf_exempt
def fetch_student_result(request):
    try:
        subject_id = request.POST.get('subject')
        student_id = request.POST.get('student')
        student = get_object_or_404(Student, id=student_id)
        subject = get_object_or_404(Subject, id=subject_id)
        result = StudentResult.objects.get(student=student, subject=subject)
        result_data = {
            'exam': result.exam,
            'test': result.test
        }
        return HttpResponse(json.dumps(result_data))
    except Exception as e:
        return HttpResponse('False')

# >------------------------HOD_VIEWS---------------------------------<

@login_required
def admin_home(request):
    total_faculty = Faculty.objects.all().count()
    total_students = Student.objects.all().count()
    subjects = Subject.objects.all()
    total_subject = subjects.count()
    total_course = Course.objects.all().count()
    attendance_list = Attendance.objects.filter(subject__in=subjects)
    total_attendance = attendance_list.count()
    attendance_list = []
    subject_list = []
    for subject in subjects:
        attendance_count = Attendance.objects.filter(subject=subject).count()
        subject_list.append(subject.name[:7])
        attendance_list.append(attendance_count)
    context = {
        'page_title': "Administrative Dashboard",
        'total_students': total_students,
        'total_faculty': total_faculty,
        'total_course': total_course,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list
    }
    return render(request,'hod/home.html',context)

def add_faculty(request):
    form = FacultyForm(request.POST or None, request.FILES or None)
    context = {'form': form, 'page_title': 'Add Faculty'}
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password')
            course = form.cleaned_data.get('course')
            passport = request.FILES.get('profile_pic')
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=2, first_name=first_name, last_name=last_name, profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.faculty.course = course
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_faculty'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Please fulfil all requirements")
    return render(request,'hod/add_faculty.html',context)

def add_student(request):
    student_form = StudentForm(request.POST or None, request.FILES or None)
    context = {'form': student_form, 'page_title': 'Add Student'}
    if request.method == 'POST':
        if student_form.is_valid():
            first_name = student_form.cleaned_data.get('first_name')
            last_name = student_form.cleaned_data.get('last_name')
            address = student_form.cleaned_data.get('address')
            email = student_form.cleaned_data.get('email')
            gender = student_form.cleaned_data.get('gender')
            password = student_form.cleaned_data.get('password')
            course = student_form.cleaned_data.get('course')
            session = student_form.cleaned_data.get('session')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=3, first_name=first_name, last_name=last_name, profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.student.session = session
                user.student.course = course
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_student'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'hod/add_student.html', context)


def add_course(request):
    form = CourseForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Course'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            try:
                course = Course()
                course.name = name
                course.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_course'))
            except:
                messages.error(request, "Could Not Add")
        else:
            messages.error(request, "Could Not Add")
    return render(request, 'hod/add_course.html', context)

def add_subject(request):
    form = SubjectForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Subject'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            course = form.cleaned_data.get('course')
            faculty = form.cleaned_data.get('faculty')
            try:
                subject = Subject()
                subject.name = name
                subject.faculty = faculty
                subject.course = course
                subject.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_subject'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")

    return render(request, 'hod/add_subject.html', context)



def manage_faculty(request):
    allFaculty = CustomUser.objects.filter(user_type=2)
    context = {
        'allFaculty': allFaculty,
        'page_title': 'Manage Faculty'
    }
    return render(request, "hod/manage_faculty.html", context)


def manage_student(request):
    students = CustomUser.objects.filter(user_type=3)
    context = {
        'students': students,
        'page_title': 'Manage Students'
    }
    return render(request, "hod/manage_student.html", context)


def manage_course(request):
    courses = Course.objects.all()
    context = {
        'courses': courses,
        'page_title': 'Manage Courses'
    }
    return render(request, "hod/manage_course.html", context)


def manage_subject(request):
    subjects = Subject.objects.all()
    context = {
        'subjects': subjects,
        'page_title': 'Manage Subjects'
    }
    return render(request, "hod/manage_subject.html", context)

def edit_faculty(request, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id)
    form = FacultyForm(request.POST or None, instance=faculty)
    context = {
        'form': form,
        'faculty_id': faculty_id,
        'page_title': 'Edit Faculty'
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            course = form.cleaned_data.get('course')
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=faculty.admin.id)
                user.username = username
                user.email = email
                if password != None:
                    user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.first_name = first_name
                user.last_name = last_name
                user.gender = gender
                user.address = address
                faculty.course = course
                user.save()
                faculty.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_faculty', args=[faculty_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please fil form properly")
    else:
        user = CustomUser.objects.get(id=faculty_id)
        faculty = Faculty.objects.get(id=user.id)
        return render(request, "hod/edit_faculty.html", context)

def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    form = StudentForm(request.POST or None, instance=student)
    context = {
        'form': form,
        'student_id': student_id,
        'page_title': 'Edit Student'
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            course = form.cleaned_data.get('course')
            session = form.cleaned_data.get('session')
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=student.admin.id)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.username = username
                user.email = email
                if password != None:
                    user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                student.session = session
                user.gender = gender
                user.address = address
                student.course = course
                user.save()
                student.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_student', args=[student_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "hod/edit_student.html", context)

# def edit_course(request, course_id):
#     instance = get_object_or_404(Course, id=course_id)
#     form = CourseForm(request.POST or None, instance=instance)
#     context = {
#         'form': form,
#         'course_id': course_id,
#         'page_title': 'Edit Course'
#     }
#     if request.method == 'POST':
#         if form.is_valid():
#             name = form.cleaned_data.get('name')
#             try:
#                 course = Course.objects.get(id=course_id)
#                 course.name = name
#                 course.save()
#                 messages.success(request, "Successfully Updated")
#             except:
#                 messages.error(request, "Could Not Update")
#         else:
#             messages.error(request, "Could Not Update")
#     return render(request, 'hod/edit_course.html', context)


def edit_course(request, course_id):
    instance = get_object_or_404(Course, id=course_id)
    form = CourseForm(request.POST or None, instance=instance)

    # Fetch the subjects related to the course
    subjects = Subject.objects.filter(course=instance)

    if request.method == 'POST':
        if form.is_valid():
            form.save()  # This will update the instance directly
            messages.success(request, "Successfully Updated")
            return render(request, 'hod/edit_course.html', {'form': form, 'subjects': subjects, 'course_id': course_id, 'page_title': 'Edit Course'})
        else:
            messages.error(request, "Could Not Update")

    context = {
        'form': form,
        'subjects': subjects,
        'course_id': course_id,
        'page_title': 'Edit Course'
    }
    return render(request, 'hod/edit_course.html', context)


def edit_subject(request, subject_id):
    instance = get_object_or_404(Subject, id=subject_id)
    form = SubjectForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'subject_id': subject_id,
        'course_id': instance.course.id,
        'page_title': 'Edit Subject'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            course = form.cleaned_data.get('course')
            faculty = form.cleaned_data.get('faculty')
            try:
                subject = Subject.objects.get(id=subject_id)
                subject.name = name
                subject.faculty = faculty
                subject.course = course
                subject.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_subject', args=[subject_id]))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'hod/edit_subject.html', context)



def add_session(request):
    form = SessionForm(request.POST or None)
    context = {'form': form, 'page_title': 'Add Session'}
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Session Created")
                return redirect(reverse('add_session'))
            except Exception as e:
                messages.error(request, 'Could Not Add ' + str(e))
        else:
            messages.error(request, 'Fill Form Properly ')
    return render(request, "hod/add_session.html", context)

def manage_session(request):
    sessions = Session.objects.all()
    context = {'sessions': sessions, 'page_title': 'Manage Sessions'}
    return render(request, "hod/manage_session.html", context)


def edit_session(request, session_id):
    instance = get_object_or_404(Session, id=session_id)
    form = SessionForm(request.POST or None, instance=instance)
    context = {'form': form, 'session_id': session_id,
               'page_title': 'Edit Session'}
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Session Updated")
                return redirect(reverse('edit_session', args=[session_id]))
            except Exception as e:
                messages.error(
                    request, "Session Could Not Be Updated " + str(e))
                return render(request, "hod/edit_session.html", context)
        else:
            messages.error(request, "Invalid Form Submitted ")
            return render(request, "hod/edit_session.html", context)

    else:
        return render(request, "hod/edit_session.html", context)
    
@csrf_exempt
def check_email_availability(request):
    email = request.POST.get("email")
    try:
        user = CustomUser.objects.filter(email=email).exists()
        if user:
            return HttpResponse(True)
        return HttpResponse(False)
    except Exception as e:
        return HttpResponse(False)
    
    
@csrf_exempt
def student_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackStudent.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Student Feedback Messages'
        }
        return render(request, 'hod/student_feedback.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackStudent, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)

@csrf_exempt
def faculty_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackFaculty.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Faculty Feedback Messages'
        }
        return render(request, 'hod/faculty_feedback.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackFaculty, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)
        
@csrf_exempt
def view_faculty_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportFaculty.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'Leave Applications From Faculty'
        }
        return render(request, "hod/faculty_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportFaculty, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False

@csrf_exempt
def view_student_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportStudent.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'Leave Applications From Students'
        }
        return render(request, "hod/student_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportStudent, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False
        
def admin_view_attendance(request):
    subjects = Subject.objects.all()
    sessions = Session.objects.all()
    context = {
        'subjects': subjects,
        'sessions': sessions,
        'page_title': 'View Attendance'
    }

    return render(request, "hod/admin_view_attendance.html", context)

@csrf_exempt
def get_admin_attendance(request):
    subject_id = request.POST.get('subject')
    session_id = request.POST.get('session')
    attendance_date_id = request.POST.get('attendance_date_id')
    try:
        subject = get_object_or_404(Subject, id=subject_id)
        session = get_object_or_404(Session, id=session_id)
        attendance = get_object_or_404(
            Attendance, id=attendance_date_id, session=session)
        attendance_reports = AttendanceReport.objects.filter(
            attendance=attendance)
        json_data = []
        for report in attendance_reports:
            data = {
                "status":  str(report.status),
                "name": str(report.student)
            }
            json_data.append(data)
        return JsonResponse(json.dumps(json_data), safe=False)
    except Exception as e:
        return None

def admin_view_profile(request):
    admin = get_object_or_404(Admin, admin=request.user)
    form = AdminForm(request.POST or None, request.FILES or None,
                     instance=admin)
    context = {'form': form,
               'page_title': 'View/Edit Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                passport = request.FILES.get('profile_pic') or None
                custom_user = admin.admin
                if password != None:
                    custom_user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    custom_user.profile_pic = passport_url
                custom_user.first_name = first_name
                custom_user.last_name = last_name
                custom_user.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('admin_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
    return render(request, "hod/admin_view_profile.html", context)



def admin_notify_faculty(request):
    faculty = CustomUser.objects.filter(user_type=2)
    context = {
        'page_title': "Send Notifications To Faculty",
        'allFaculty': faculty
    }
    return render(request, "hod/faculty_notification.html", context)

def admin_notify_student(request):
    student = CustomUser.objects.filter(user_type=3)
    context = {
        'page_title': "Send Notifications To Students",
        'students': student
    }
    return render(request, "hod/student_notification.html", context)

@csrf_exempt
def send_student_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    student = get_object_or_404(Student, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Student Management System",
                'body': message,
                'click_action': reverse('student_view_notification'),
                # 'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': student.admin.fcm_token
        }
        headers = {'Authorization':
                   'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationStudent(student=student, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")
    
@csrf_exempt
def send_faculty_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    faculty = get_object_or_404(Faculty, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Student Management System",
                'body': message,
                'click_action': reverse('faculty_view_notification'),
                # 'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': faculty.admin.fcm_token
        }
        headers = {'Authorization':
                   'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationFaculty(faculty=faculty, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")
    
def delete_faculty(request, faculty_id):
    faculty = get_object_or_404(CustomUser, faculty__id=faculty_id)
    faculty.delete()
    messages.success(request, "Faculty deleted successfully!")
    return redirect(reverse('manage_faculty'))

def delete_student(request, student_id):
    student = get_object_or_404(CustomUser, student__id=student_id)
    student.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect(reverse('manage_student'))

def manage_courses(request):
    # Fetch all the courses from the database
    courses = Course.objects.all()

    # Render the courses page with the list of courses
    return render(request, 'faculty/course.html', {'courses': courses})

def delete_course(request, course_id):
    print(f"Deleting course with id: {course_id}")  # Debugging line
    course = get_object_or_404(Course, id=course_id)
    try:
        course.delete()
        messages.success(request, "Course deleted successfully!")
    except Exception:
        messages.error(request, "Sorry, some students are assigned to this course already.")
    return redirect(reverse('course_list'))


def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    messages.success(request, "Subject deleted successfully!")
    return redirect(reverse('manage_subject'))

def delete_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    try:
        session.delete()
        messages.success(request, "Session deleted successfully!")
    except Exception:
        messages.error(
            request, "There are students assigned to this session. Please move them to another session.")
    return redirect(reverse('manage_session'))
# extra
def course_list(request):
    courses = Course.objects.all()# Get all courses from the database
    print([course.id for course in courses])
    context = {
        'courses': courses
    }
    return render(request, 'hod/course.html', context)

def faculty_list(request):
    faculties = Faculty.objects.select_related('course', 'admin').all()  # Optimize queries
    context = {
        'faculties': faculties
    }
    return render(request, 'hod/faculty.html', context)


def student_list(request):
    students = Student.objects.all().select_related('admin', 'course', 'session')
    print(students)
    context = {
        'students': students  # Pass the student queryset to the template
    }
    
    return render(request, 'hod/student.html', context)
# >----------------------EDIT_RESULT-----------------------<

class EditResultView(View):
    def get(self, request, *args, **kwargs):
        resultForm = EditResultForm()
        faculty = get_object_or_404(Faculty, admin=request.user)
        resultForm.fields['subject'].queryset = Subject.objects.filter(faculty=faculty)
        context = {
            'form': resultForm,
            'page_title': "Edit Student's Result"
        }
        return render(request, "faculty/edit_student_result.html", context)

    def post(self, request, *args, **kwargs):
        form = EditResultForm(request.POST)
        context = {'form': form, 'page_title': "Edit Student's Result"}
        if form.is_valid():
            try:
                student = form.cleaned_data.get('student')
                subject = form.cleaned_data.get('subject')
                test = form.cleaned_data.get('test')
                exam = form.cleaned_data.get('exam')
                # Validating
                result = StudentResult.objects.get(student=student, subject=subject)
                result.exam = exam
                result.test = test
                result.save()
                messages.success(request, "Result Updated")
                return redirect(reverse('edit_student_result'))
            except Exception as e:
                messages.warning(request, "Result Could Not Be Updated")
        else:
            messages.warning(request, "Result Could Not Be Updated")
        return render(request, "faculty/edit_student_result.html", context)
