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
    AddStdntInfoAPIView,
    StdntSchoolDetailsAPIView   
    
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
    path('addstdntinfo/',AddStdntInfoAPIView.as_view(), name = 'addstdntinfo-list'),
    path('stdntschooldetails/',StdntSchoolDetailsAPIView.as_view(), name='stdntschooldetails-list'),
    

    path('deactivate_or_modify_course/<str:id_or_offercode>/<str:deactivate>', CourseAPIView.as_view(), name='deactivate_modify_course-active'),
    path('deactivate_or_modify_department/<str:id_or_offercode>/<str:deactivate>', DepartmentAPIView.as_view(), name = 'deactivate_modify_department-active'),
    path('deactivate_or_modify_subject/<str:id_or_offercode>/<str:deactivate>',SubjInfoAPIView.as_view(), name="deactivate_modify_subject"),
    path('deactivate_or_modify_room/<str:id_or_offercode>/<str:deactivate>',RoomAPIView.as_view(), name="deactivate_modify_room"),
    path('deactivate_or_modify_staff/<str:id_or_offercode>/<str:deactivate>',StaffInfoAPIView.as_view(), name='deactivate_modify_staff'),
    path('deactivate_or_modify_addstaffinfo/<str:id_or_offercode>/<str:deactivate>',AddStaffInfoAPIView.as_view(), name='deactivate_modify_addstaffinfo'),
    path('deactivate_or_modify_schedule/<str:id_or_offercode>/<str:deactivate>', ScheduleAPIView.as_view(), name='deactivate_modify_schedule'),
    path('deactivate_or_modify_student/<str:id_or_offercode>/<str:deactivate>', StdntInfoAPIView.as_view(), name='deactivate_modify_student'),
    path('deactivate_or_modify_addstdntinfo/<str:id_or_offercode>/<str:deactivate>', StdntInfoAPIView.as_view(), name='deactivate_modify_addstdntinfo'),
    path('deactivate_or_modify_stdntschooldetails/<str:id_or_offercode>/str:deactivate',StdntSchoolDetailsAPIView.as_view(), name='deactivate_modify_stdntschooldetails'),
]
