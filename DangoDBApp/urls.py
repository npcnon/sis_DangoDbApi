from django.urls import path
from .views import RoomAPIView,CourseAPIView,DepartmentAPIView, SubjInfoAPIView

urlpatterns = [
    #path('apimymodel/', TblCourseAPIView.as_view(), name='mymodel-list'),
    path('rooms/', RoomAPIView.as_view(), name='room-list'),
    path('course/', CourseAPIView.as_view(), name = 'course-list'),
    path('department/',DepartmentAPIView.as_view(), name = 'department-list'),
    path('subject/', SubjInfoAPIView.as_view(), name= 'subject-list'),
    path('deactivate_or_modify_course/<int:id>/<str:deactivate>', CourseAPIView.as_view(), name='deactivate_modify_course-active'),
    path('deactivate_or_modify_department/<str:offercode>/<str:deactivate>', DepartmentAPIView.as_view(), name = 'deactivate_modify_department-active'),
    path('deactivate_or_modify_subject/<int:id>/<str:deactivate>',SubjInfoAPIView.as_view(), name="deactivate_modify_subject")
]
