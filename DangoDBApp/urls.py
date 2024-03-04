from django.urls import path
from .views import TblCourseAPIView

urlpatterns = [
    path('apimymodel/', TblCourseAPIView.as_view(), name='mymodel-list'),
]
