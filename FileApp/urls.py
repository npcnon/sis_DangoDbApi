from django.urls import path
from .views import (
    FileUploadView, 
    # DocumentDeleteView, 
    AdminDocumentView, 
    AdminContactView, 
    AdminContactRetrieveView,
    AdminContactListView  # We'll add this new view
)

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('documents/', FileUploadView.as_view(), name='document-list'),
    # path('delete/', DocumentDeleteView.as_view(), name='file-upload'),
    path('admin-documents/', AdminDocumentView.as_view(), name='admin-documents'),
    path('admin-contact/', AdminContactView.as_view(), name='admin-contact-create'),
    path('admin-contacts/', AdminContactListView.as_view(), name='admin-contact-list'),
    path('admin-contact/<uuid:contact_id>/', AdminContactRetrieveView.as_view(), name='admin-contact-retrieve')
]