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
from .models import Document
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
import logging

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
        try:
            print("Starting file upload process")
            if 'file' not in request.FILES:
                return Response({'error': 'No file provided'}, status=400)

            file = request.FILES['file']
            document_type = request.data.get('document_type')
            
            logger.info(f"Processing upload for document type: {document_type}")
            
            # Validate document type
            if not document_type or document_type not in dict(Document.DOCUMENT_TYPES):
                return Response({
                    'error': 'Invalid document type',
                    'valid_types': dict(Document.DOCUMENT_TYPES)
                }, status=400)

            # Check existing document
            existing_doc = Document.objects.filter(
                user=request.user,
                document_type=document_type
            ).first()
            
            if existing_doc:
                # For existing documents, try to generate a new signed URL
                signed_url, expiration = self.generate_signed_url(
                    existing_doc.cloudinary_public_id,
                    self.get_resource_type(self.validate_file_type(file), document_type)
                )
                
                response_data = {
                    'error': 'Document already submitted',
                    'status': existing_doc.status,
                    'uploaded_at': existing_doc.uploaded_at
                }
                
                if signed_url:
                    response_data.update({
                        'temporary_url': signed_url,
                        'expires_at': expiration.isoformat()
                    })
                
                return Response(response_data, status=400)

            # Validate file type
            file_type = self.validate_file_type(file)
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

            # Determine resource type
            resource_type = self.get_resource_type(file_type, document_type)

            # Upload to Cloudinary
            folder = f"user_{request.user.id}/documents/{document_type}"
            print(f"Uploading to Cloudinary folder: {folder}")
            
            try:
                upload_result = cloudinary.uploader.upload(
                    file,
                    folder=folder,
                    resource_type=resource_type,
                    type="private",
                    access_mode="authenticated",
                    secure=True
                )
                print(f"Cloudinary upload successful: {upload_result['public_id']}")
            except Exception as e:
                print(f"Cloudinary upload failed: {str(e)}")
                return Response(
                    {'error': 'Failed to upload file to storage'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Create document record
            document = Document.objects.create(
                user=request.user,
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
                'document_type': document.get_document_type_display(),
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

        except IntegrityError as e:
            print(f"IntegrityError during upload: {str(e)}")
            return Response(
                {'error': 'Document already exists for this user'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(f"Unexpected error during upload: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request, document_id=None):
        try:
            if document_id is None:
                documents = Document.objects.filter(user=request.user)
                response_data = []
                
                for doc in documents:
                    doc_data = {
                        'id': doc.id,
                        'document_type': doc.get_document_type_display(),
                        'status': doc.status,
                        'filename': doc.original_filename,
                        'uploaded_at': doc.uploaded_at,
                        'review_notes': doc.review_notes
                    }
                    
                    # Determine resource type based on document type
                    resource_type = "image" if doc.document_type == 'profile' else "raw"
                    
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