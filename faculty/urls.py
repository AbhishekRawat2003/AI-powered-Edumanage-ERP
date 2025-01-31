# faculty/urls.py
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'faculty'

urlpatterns = [
     # faculty
    path("faculty/home/",faculty_home,name='faculty_home'),
#     path("home",faculty_home,name='faculty_home'),
    path("faculty/apply/leave",faculty_apply_leave,name='faculty_apply_leave'),
    path("faculty/feedback/", faculty_feedback, name='faculty_feedback'),
    path("faculty/view/profile/", faculty_view_profile,
         name='faculty_view_profile'),
    path("faculty/attendance/take/", faculty_take_attendance,
         name='faculty_take_attendance'),
    path("faculty/attendance/update/", faculty_update_attendance,
         name='faculty_update_attendance'), #not added
    path("faculty/get_students/", get_students, name='get_students'),
    path("faculty/attendance/fetch/", get_student_attendance,
         name='get_student_attendance'),# notadded
    path("faculty/attendance/save/",
         save_attendance, name='save_attendance'),#not added
    path("faculty/attendance/update/",
         update_attendance, name='update_attendance'),
    path("faculty/fcmtoken/", faculty_fcmtoken, name='faculty_fcmtoken'), #not added
    path("faculty/view/notification/", faculty_view_notification,
         name="faculty_view_notification"),
    path("faculty/result/add/", faculty_add_result, name='faculty_add_result'),
    path("faculty/result/edit/", EditResultView.as_view(),
         name='edit_student_result'), #not added
    path('faculty/result/fetch/', fetch_student_result,
         name='fetch_student_result'), #not added
#     extra
     path('faculty/get_students/', get_students, name='get_students'),

     # HOD --------------------------
     path("admin/home/", admin_home, name='admin_home'),
     path("faculty/add", add_faculty, name='add_faculty'),
    path("course/add", add_course, name='add_course'),
    path("send_student_notification/", send_student_notification,
         name='send_student_notification'),
    path("send_faculty_notification/", send_faculty_notification,
         name='send_faculty_notification'),
    path("add_session/", add_session, name='add_session'),
    path("admin_notify_student", admin_notify_student,
         name='admin_notify_student'),
    path("admin_notify_faculty", admin_notify_faculty,
         name='admin_notify_faculty'),
    path("faculty/admin_view_profile", admin_view_profile,
         name='admin_view_profile'),
    path("check_email_availability", check_email_availability,
         name="check_email_availability"),
    path("session/manage/", manage_session, name='manage_session'),
    path("session/edit/<int:session_id>",
         edit_session, name='edit_session'),
    path("student/view/feedback/", student_feedback_message,
         name="student_feedback_message",),
    path("faculty/view/feedback/", faculty_feedback_message,
         name="faculty_feedback_message",),
    path("student/view/leave/", view_student_leave,
         name="view_student_leave",),
    path("faculty/view/leave/", view_faculty_leave, name="view_faculty_leave",),
    path("attendance/view/", admin_view_attendance,
         name="admin_view_attendance",),
    path("attendance/fetch/", get_admin_attendance,
         name='get_admin_attendance'),
    path("student/add/", add_student, name='add_student'),
    path("subject/add/", add_subject, name='add_subject'),
    path("faculty/manage/", manage_faculty, name='manage_faculty'),
    path("student/manage/", manage_student, name='manage_student'),
    path("course/manage/", manage_course, name='manage_course'),
    path("subject/manage/", manage_subject, name='manage_subject'),
    path("faculty/edit/<int:faculty_id>", edit_faculty, name='edit_faculty'),
    path("faculty/delete/<int:faculty_id>",
         delete_faculty, name='delete_faculty'),

    path("course/delete/<int:course_id>",
         delete_course, name='delete_course'),

    path("subject/delete/<int:subject_id>",
         delete_subject, name='delete_subject'),

    path("session/delete/<int:session_id>",
         delete_session, name='delete_session'),

    path("student/delete/<int:student_id>",
         delete_student, name='delete_student'),
    path("student/edit/<int:student_id>",
         edit_student, name='edit_student'),
    path("course/edit/<int:course_id>",
         edit_course, name='edit_course'),
    path("subject/edit/<int:subject_id>",
         edit_subject, name='edit_subject'),
    
    
    
#     extra 
     path("courses",course_list,name="course_list"),
     path("faculty",faculty_list,name="faculty_list"),
     path("student", student_list, name="student_list"),
     path('courses/', manage_courses, name='manage_courses'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)