from rest_framework import serializers

from FileApp.models import AdminContact, AdminContactDocument

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()



class AdminContactDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminContactDocument
        fields = [
            'id', 
            'file_name', 
            'document_type', 
            'uploaded_at', 
            'file_size', 
            'mime_type'
        ]
        read_only_fields = ['id', 'uploaded_at']

class AdminContactSerializer(serializers.ModelSerializer):
    documents = AdminContactDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = AdminContact
        fields = [
            'id', 
            'message', 
            'created_at', 
            'updated_at', 
            'status', 
            'documents'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'status']