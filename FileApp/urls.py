# FileApp/urls.py
from django.urls import path
from .views import FileUploadView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('documents/', FileUploadView.as_view(), name='document-list'),
    path('documents/<int:document_id>/', FileUploadView.as_view(), name='document-detail'),
]