from django.urls import path
from .views import RoomAPIView,CourseAPIView,DepartmentAPIView

urlpatterns = [
    #path('apimymodel/', TblCourseAPIView.as_view(), name='mymodel-list'),
    path('rooms/', RoomAPIView.as_view(), name='room-list'),
    path('course/', CourseAPIView.as_view(), name = 'course-list'),
    path('department/',DepartmentAPIView.as_view(), name = 'department-list'),
    path('deactivate_course/<int:id>/', CourseAPIView.as_view(), name='deactivatecourse-active'),
    path('deactivate_department/<int:id>/<str:deactivate>', DepartmentAPIView.as_view(), name = 'deactivatedepartment-active')
]
