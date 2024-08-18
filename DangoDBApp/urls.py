#DangoDBApp.urls

from django.urls import path
from .views import (
    RoomAPIView,
    CourseAPIView,
    DepartmentAPIView, 
    SubjInfoAPIView,
    StaffInfoAPIView, 
    AddStaffInfoAPIView,
    ScheduleAPIView,
    StdntInfoAPIView,
    StudentPersonalDataAPIView,
    StudentFamilyAPIView,
    StudentAcademicBackgroundAPIView,
    StudentAcademicHistoryAPIView,
    )

urlpatterns = [
    #path('apimymodel/', TblCourseAPIView.as_view(), name='mymodel-list'),
    path('room/', RoomAPIView.as_view(), name='room-list'),
    path('course/', CourseAPIView.as_view(), name = 'course-list'),
    path('department/',DepartmentAPIView.as_view(), name = 'department-list'),
    path('subject/', SubjInfoAPIView.as_view(), name= 'subject-list'),
    path('staff/',StaffInfoAPIView.as_view(), name='staff-list'),
    path('addstaffinfo/',AddStaffInfoAPIView.as_view(), name='addstaffinfo-list'),
    path('schedule/', ScheduleAPIView.as_view(), name = 'schedule-list'),
    path('student/', StdntInfoAPIView.as_view(), name = 'student-list'),
    path('stdntpersonal/',StudentPersonalDataAPIView.as_view(),name = 'student-personal-list'),
    path('stdntfamily/',StudentFamilyAPIView.as_view(),name = 'student-family-list'),
    path('stdntacademicbackground/',StudentAcademicBackgroundAPIView.as_view(),name = 'student-academicbackground-list'),
    path('stdntacademichistory/',StudentAcademicHistoryAPIView.as_view(),name = 'student-academichistory-list'),


    path('deactivate_or_modify_course/<str:id_or_offercode>/<str:deactivate>', CourseAPIView.as_view(), name='deactivate_modify_course-active'),
    path('deactivate_or_modify_department/<str:id_or_offercode>/<str:deactivate>', DepartmentAPIView.as_view(), name = 'deactivate_modify_department-active'),
    path('deactivate_or_modify_subject/<str:id_or_offercode>/<str:deactivate>',SubjInfoAPIView.as_view(), name="deactivate_modify_subject"),
    path('deactivate_or_modify_room/<str:id_or_offercode>/<str:deactivate>',RoomAPIView.as_view(), name="deactivate_modify_room"),
    path('deactivate_or_modify_staff/<str:id_or_offercode>/<str:deactivate>',StaffInfoAPIView.as_view(), name='deactivate_modify_staff'),
    path('deactivate_or_modify_addstaffinfo/<str:id_or_offercode>/<str:deactivate>',AddStaffInfoAPIView.as_view(), name='deactivate_modify_addstaffinfo'),
    path('deactivate_or_modify_schedule/<str:id_or_offercode>/<str:deactivate>', ScheduleAPIView.as_view(), name='deactivate_modify_schedule'),
    path('deactivate_or_modify_student/<str:id_or_offercode>/<str:deactivate>', StdntInfoAPIView.as_view(), name='deactivate_modify_student'),
    path('deactivate_or_modify_addstdntinfo/<str:id_or_offercode>/<str:deactivate>', StdntInfoAPIView.as_view(), name='deactivate_modify_addstdntinfo'),    
    
    path('deactivate_or_modify_stdntpersonal/<str:id_or_offercode>/str:deactivate',StudentPersonalDataAPIView.as_view(),name = 'dm-student-personal'),
    path('deactivate_or_modify_stdntfamily/<str:id_or_offercode>/str:deactivate',StudentFamilyAPIView.as_view(),name = 'dm-student-family'),
    path('deactivate_or_modify_stdntacademicbackground/<str:id_or_offercode>/str:deactivate',StudentAcademicBackgroundAPIView.as_view(),name = 'dm-student-academic-background'),
    path('deactivate_or_modify_stdntacademichistory/<str:id_or_offercode>/str:deactivate',StudentAcademicHistoryAPIView.as_view(),name = 'dm-student-academic-history'),

]   
