from django.urls import path
from .views import RoomAPIView,CourseAPIView,DepartmentAPIView

urlpatterns = [
    #path('apimymodel/', TblCourseAPIView.as_view(), name='mymodel-list'),
    path('rooms/', RoomAPIView.as_view(), name='room-list'),
    path('course/', CourseAPIView.as_view(), name = 'course-list'),
    path('department/',DepartmentAPIView.as_view(), name = 'department-list')

]
