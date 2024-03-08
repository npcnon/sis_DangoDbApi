from django.urls import path
from .views import RoomAPIView,CourseAPIView

urlpatterns = [
    #path('apimymodel/', TblCourseAPIView.as_view(), name='mymodel-list'),
    path('rooms/', RoomAPIView.as_view(), name='room-list'),
    path('course/', CourseAPIView.as_view(), name = 'course-list')

]
