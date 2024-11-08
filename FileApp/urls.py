# FileApp/urls.py
from django.urls import path
from .views import FileUploadView
from .document_delete_view import DocumentDeleteView
from .views import AdminDocumentView
urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('documents/', FileUploadView.as_view(), name='document-list'),
    path('documents/<int:document_id>/', FileUploadView.as_view(), name='document-detail'),
    path('delete/', DocumentDeleteView.as_view(), name='file-upload'),
    path('admin-documents/', AdminDocumentView.as_view(), name='admin-documents'),
    path('admin-documents', AdminDocumentView.as_view(), name='admin-documents'),

]