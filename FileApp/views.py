from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.authentication import JWTAuthentication
import cloudinary.uploader
import cloudinary.utils
import magic
from datetime import datetime, timedelta
from rest_framework.response import Response
from django.db import transaction
from typing import Dict, Any, Tuple

from users.models import User
from .models import Document
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
import logging
from DangoDBApp.models import TblStudentPersonalData
from DangoDBApp.serializers import TblStudentPersonalDataSerializer

logger = logging.getLogger(__name__)

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    ALLOWED_MIME_TYPES = {
        'application/pdf': '.pdf',
        'image/jpeg': '.jpg',
        'image/png': '.png'
    }
    #TODO: fix pdf viewing
    def generate_signed_url(self, public_id, resource_type="image"):
        """Generate a signed URL for private Cloudinary resources"""
        expiration = datetime.now() + timedelta(hours=1)
        
        try:
            signed_url = cloudinary.utils.cloudinary_url(
                public_id,
                type="private",
                resource_type=resource_type,
                secure=True,
                sign_url=True,
                expires_at=int(expiration.timestamp())
            )[0]
            print(f"Generated signed URL for {public_id}")
            return signed_url, expiration
        except Exception as e:
            print(f"Error generating signed URL for {public_id}: {str(e)}")
            return None, None

    def validate_file_type(self, file):
        try:
            file_magic = magic.Magic(mime=True)
            file_type = file_magic.from_buffer(file.read(2048))
            file.seek(0)
            print(f"Detected file type: {file_type}")
            return file_type
        except Exception as e:
            print(f"Error validating file type: {str(e)}")
            raise

    def get_resource_type(self, file_type, document_type):
        """Determine Cloudinary resource type based on file and document type"""
        if document_type == 'profile':
            return 'image'
        if file_type.startswith('image/'):
            return 'image'
        return 'raw'

    def post(self, request):
        print(f"request data: {request.data}")
        print(f"Starting file upload process for user: {request.user.id}")
        
        try:
            # Validate request has file
            if 'file' not in request.FILES:
                logger.warning("Upload attempt with no file provided")
                return Response({
                    'error': 'No file provided',
                    'code': 'FILE_MISSING',
                    'details': 'Please attach a file to your request'
                }, status=400)

            file = request.FILES['file']
            document_type = request.data.get('document_type')
            
            # Log initial request details
            logger.info(f"Upload request received - File: {file.name}, Type: {document_type}, Size: {file.size}")

            # Validate document type
            if not document_type:
                logger.warning("Upload attempt with missing document type")
                return Response({
                    'error': 'Document type not provided',
                    'code': 'DOCUMENT_TYPE_MISSING',
                    'valid_types': dict(Document.DOCUMENT_TYPES)
                }, status=400)
                
            if document_type not in dict(Document.DOCUMENT_TYPES):
                logger.warning(f"Invalid document type provided: {document_type}")
                return Response({
                    'error': 'Invalid document type',
                    'code': 'INVALID_DOCUMENT_TYPE',
                    'valid_types': dict(Document.DOCUMENT_TYPES),
                    'provided_type': document_type
                }, status=400)

            # Check for existing document
            existing_doc = Document.objects.filter(
                user=request.user,
                document_type=document_type
            ).first()
            
            if existing_doc:
                logger.info(f"Duplicate document upload attempt for type: {document_type}")
                try:
                    signed_url, expiration = self.generate_signed_url(
                        existing_doc.cloudinary_public_id,
                        self.get_resource_type(self.validate_file_type(file), document_type)
                    )
                    
                    response_data = {
                        'error': 'Document already submitted',
                        'code': 'DUPLICATE_DOCUMENT',
                        'status': existing_doc.status,
                        'uploaded_at': existing_doc.uploaded_at,
                        'document_id': existing_doc.id
                    }
                    
                    if signed_url:
                        response_data.update({
                            'temporary_url': signed_url,
                            'expires_at': expiration.isoformat()
                        })
                    
                    return Response(response_data, status=400)
                except Exception as e:
                    logger.error(f"Error generating signed URL for existing document: {str(e)}")
                    return Response({
                        'error': 'Error accessing existing document',
                        'code': 'EXISTING_DOCUMENT_ACCESS_ERROR',
                        'details': str(e)
                    }, status=500)

            # Validate file type
            try:
                file_type = self.validate_file_type(file)
                if file_type not in self.ALLOWED_MIME_TYPES:
                    logger.warning(f"Invalid file type uploaded: {file_type}")
                    return Response({
                        'error': 'Invalid file type',
                        'code': 'INVALID_FILE_TYPE',
                        'allowed_types': list(self.ALLOWED_MIME_TYPES.keys()),
                        'provided_type': file_type
                    }, status=400)
            except Exception as e:
                logger.error(f"Error validating file type: {str(e)}")
                return Response({
                    'error': 'File type validation failed',
                    'code': 'FILE_TYPE_VALIDATION_ERROR',
                    'details': str(e)
                }, status=400)

            # Validate file size
            if file.size > 10 * 1024 * 1024:
                logger.warning(f"File size too large: {file.size} bytes")
                return Response({
                    'error': 'File too large',
                    'code': 'FILE_TOO_LARGE',
                    'max_size': '10MB',
                    'provided_size': f"{file.size / (1024 * 1024):.2f}MB"
                }, status=400)

            # Upload to Cloudinary
            folder = f"user_{request.user.id}/documents/{document_type}"
            logger.info(f"Attempting Cloudinary upload to folder: {folder}")
            
            try:
                resource_type = self.get_resource_type(file_type, document_type)
                upload_result = cloudinary.uploader.upload(
                    file,
                    folder=folder,
                    resource_type=resource_type,
                    type="private",
                    access_mode="authenticated",
                    secure=True
                )
                logger.info(f"Cloudinary upload successful: {upload_result['public_id']}")
            except cloudinary.exceptions.Error as e:
                logger.error(f"Cloudinary upload failed: {str(e)}")
                return Response({
                    'error': 'Storage upload failed',
                    'code': 'CLOUDINARY_UPLOAD_ERROR',
                    'details': str(e)
                }, status=500)
            except Exception as e:
                logger.error(f"Unexpected error during Cloudinary upload: {str(e)}")
                return Response({
                    'error': 'Unexpected error during file upload',
                    'code': 'UPLOAD_ERROR',
                    'details': str(e)
                }, status=500)

            # Create document record
            try:
                document = Document.objects.create(
                    user=request.user,
                    file_type=file_type,
                    cloudinary_public_id=upload_result['public_id'],
                    document_type=document_type,
                    original_filename=file.name,
                    status='pending'
                )
                logger.info(f"Document record created successfully: {document.id}")
            except IntegrityError as e:
                logger.error(f"Database integrity error: {str(e)}")
                return Response({
                    'error': 'Document already exists for this user',
                    'code': 'DATABASE_INTEGRITY_ERROR',
                    'details': str(e)
                }, status=400)
            except Exception as e:
                logger.error(f"Database error during document creation: {str(e)}")
                return Response({
                    'error': 'Failed to create document record',
                    'code': 'DATABASE_ERROR',
                    'details': str(e)
                }, status=500)

            # Generate signed URL
            try:
                signed_url, expiration = self.generate_signed_url(
                    upload_result['public_id'],
                    resource_type
                )

                response_data = {
                    'id': document.id,
                    'document_type': document.get_document_type_display(),
                    'file_type': document.file_type,
                    'status': document.status,
                    'filename': document.original_filename,
                    'uploaded_at': document.uploaded_at
                }

                if signed_url:
                    response_data.update({
                        'temporary_url': signed_url,
                        'expires_at': expiration.isoformat()
                    })

                logger.info(f"Document upload process completed successfully: {document.id}")
                return Response(response_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Error generating signed URL: {str(e)}")
                return Response({
                    'error': 'Failed to generate access URL',
                    'code': 'URL_GENERATION_ERROR',
                    'details': str(e)
                }, status=500)

        except Exception as e:
            logger.error(f"Unexpected error in upload process: {str(e)}")
            return Response({
                'error': 'Internal server error',
                'code': 'INTERNAL_SERVER_ERROR',
                'details': str(e)
            }, status=500)

    def get(self, request, document_id=None):
        try:
            
            if document_id is None:
                print(f"request: {request.query_params}")
                documents = Document.objects.filter(user=request.user)
                response_data = []
                
                for doc in documents:
                    doc_data = {
                        'id': doc.id,
                        'document_type': doc.get_document_type_display(),
                        'file_type': doc.file_type,
                        'status': doc.status,
                        'filename': doc.original_filename,
                        'uploaded_at': doc.uploaded_at,
                        'review_notes': doc.review_notes
                    }
                    
                    # Determine resource type based on document type
                    resource_type = "image" if doc.file_type.startswith('image/') else "raw"
                    
                    signed_url, expiration = self.generate_signed_url(
                        doc.cloudinary_public_id,
                        resource_type
                    )
                    
                    if signed_url:
                        doc_data.update({
                            'temporary_url': signed_url,
                            'expires_at': expiration.isoformat()
                        })
                    
                    response_data.append(doc_data)
                
                return Response({'documents': response_data})
            
            document = get_object_or_404(Document, id=document_id, user=request.user)
            resource_type = "image" if document.document_type == 'profile' else "raw"
            
            signed_url, expiration = self.generate_signed_url(
                document.cloudinary_public_id,
                resource_type
            )
            
            if not signed_url:
                print(f"Failed to generate signed URL for document {document_id}")
                return Response(
                    {'error': 'Failed to generate document access URL'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            return Response({
                'id': document.id,
                'document_type': document.get_document_type_display(),
                'status': document.status,
                'filename': document.original_filename,
                'uploaded_at': document.uploaded_at,
                'review_notes': document.review_notes,
                'temporary_url': signed_url,
                'expires_at': expiration.isoformat()
            })
            
        except Exception as e:
            print(f"Error retrieving document: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve document'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

        



        
class AdminDocumentView(APIView):
    """Public view to post and retrieve documents without authentication."""
    
    parser_classes = (MultiPartParser, FormParser)

    ALLOWED_MIME_TYPES = {
        'application/pdf': '.pdf',
        'image/jpeg': '.jpg',
        'image/png': '.png'
    }

    def generate_signed_url(self, public_id, resource_type="image"):
        """Generate a signed URL for private Cloudinary resources."""
        expiration = datetime.now() + timedelta(hours=1)
        try:
            signed_url = cloudinary.utils.cloudinary_url(
                public_id,
                type="private",
                resource_type=resource_type,
                secure=True,
                sign_url=True,
                expires_at=int(expiration.timestamp())
            )[0]
            return signed_url, expiration
        except Exception as e:
            logger.error(f"Error generating signed URL for {public_id}: {str(e)}")
            return None, None

    def validate_file_type(self, file):
        """Validate the uploaded file type."""
        try:
            file_magic = magic.Magic(mime=True)
            file_type = file_magic.from_buffer(file.read(2048))
            file.seek(0)
            print(f'file type: {file_type}')
            return file_type
        except Exception as e:
            logger.error(f"Error validating file type: {str(e)}")
            raise
        

    def get_resource_type(self, file_type, document_type):
        """Determine Cloudinary resource type based on file and document type."""
        print(f'document type: {document_type} \n file type {file_type}')
        if document_type == 'profile':
            return 'image'
        if file_type.startswith('image/'):
            return 'image'
        return 'raw'

    def post(self, request):
        print(f'request data: {request.data}')
        try:
            logger.info("Starting public file upload process")
            
            # Validate required fields
            if 'file' not in request.FILES:
                return Response({'error': 'No file provided'}, status=400)
            if 'email' not in request.data:
                return Response({'error': 'Fulldata Applicant ID is required'}, status=400)
            if 'document_type' not in request.data:
                return Response({'error': 'Document type is required'}, status=400)

            file = request.FILES['file']
            email = request.data['email']
            document_type = request.data['document_type']

            # Get or create user
            user, created = User.objects.get_or_create(email=email)
            
            # Validate document type
            if document_type not in dict(Document.DOCUMENT_TYPES):
                return Response({
                    'error': 'Invalid document type',
                    'valid_types': dict(Document.DOCUMENT_TYPES)
                }, status=400)

            # Check existing document
            existing_doc = Document.objects.filter(
                user=user,
                document_type=document_type
            ).first()

            if existing_doc:
                return Response({
                    'error': 'Document already exists for this user',
                    'status': existing_doc.status,
                    'uploaded_at': existing_doc.uploaded_at
                }, status=400)

            # Validate file type
            file_type = self.validate_file_type(file)
            print(f"Detected file type: {file_type}")
            if file_type not in self.ALLOWED_MIME_TYPES:
                return Response({
                    'error': 'Invalid file type',
                    'allowed_types': list(self.ALLOWED_MIME_TYPES.keys())
                }, status=400)

            # Validate file size (10MB limit)
            if file.size > 10 * 1024 * 1024:
                return Response({
                    'error': 'File too large',
                    'max_size': '10MB'
                }, status=400)

            # Determine resource type and upload to Cloudinary
            resource_type = self.get_resource_type(file_type, document_type)
            folder = f"user_{user.id}/documents/{document_type}"
            
            try:
                upload_result = cloudinary.uploader.upload(
                    file,
                    folder=folder,
                    resource_type=resource_type,
                    type="private",
                    access_mode="authenticated",
                    secure=True
                )
            except Exception as e:
                logger.error(f"Cloudinary upload failed: {str(e)}")
                return Response(
                    {'error': 'Failed to upload file to storage'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Create document record
            document = Document.objects.create(
                user=user,
                file_type=file_type,
                cloudinary_public_id=upload_result['public_id'],
                document_type=document_type,
                original_filename=file.name,
                status='pending'
            )

            # Generate signed URL
            signed_url, expiration = self.generate_signed_url(
                upload_result['public_id'],
                resource_type
            )

            response_data = {
                'id': document.id,
                'email': user.email,
                'document_type': document.get_document_type_display(),
                'file_type': document.file_type,
                'status': document.status,
                'filename': document.original_filename,
                'uploaded_at': document.uploaded_at
            }

            if signed_url:
                response_data.update({
                    'temporary_url': signed_url,
                    'expires_at': expiration.isoformat()
                })

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Unexpected error during upload: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request):
        try:
            email = request.query_params.get('email')
            document_type = request.query_params.get('document_type')
            
            documents = Document.objects.all()
            
            if email:
                documents = documents.filter(user__email=email)
            
            if document_type:
                documents = documents.filter(document_type=document_type)
            
            response_data = []

            for doc in documents:
                doc_data = {
                    'id': doc.id,
                    'email': doc.user.email,
                    'document_type': doc.get_document_type_display(),
                    'status': doc.status,
                    'filename': doc.original_filename,
                    'uploaded_at': doc.uploaded_at,
                    'review_notes': doc.review_notes
                }

                resource_type = "image" if doc.file_type.startswith('image/') else "raw"
                signed_url, expiration = self.generate_signed_url(
                    doc.cloudinary_public_id,
                    resource_type
                )

                if signed_url:
                    doc_data.update({
                        'temporary_url': signed_url,
                        'expires_at': expiration.isoformat()
                    })

                response_data.append(doc_data)

            return Response({'documents': response_data}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve documents'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




