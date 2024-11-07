from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import cloudinary.uploader
from .models import Document
import logging

logger = logging.getLogger(__name__)

class DocumentDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete_from_cloudinary(self, public_id, resource_type="raw"):
        """Delete a file from Cloudinary storage"""
        try:
            result = cloudinary.uploader.destroy(
                public_id,
                resource_type=resource_type,
                invalidate=True
            )
            logger.info(f"Successfully deleted {public_id} from Cloudinary")
            return result
        except Exception as e:
            logger.error(f"Failed to delete {public_id} from Cloudinary: {str(e)}")
            raise

    def delete(self, request, document_id=None):
        """Delete a single document or all documents for the user"""
        try:
            if document_id:
                # Delete single document
                document = Document.objects.get(id=document_id, user=request.user)
                
                # Determine resource type based on document type
                resource_type = "image" if document.document_type == 'profile' else "raw"
                
                # Delete from Cloudinary
                self.delete_from_cloudinary(document.cloudinary_public_id, resource_type)
                
                # Delete from database
                document.delete()
                
                return Response({
                    'message': f'Document {document_id} successfully deleted'
                }, status=status.HTTP_200_OK)
            
            else:
                # Delete all documents for the user
                documents = Document.objects.filter(user=request.user)
                deleted_count = 0
                failed_count = 0
                
                for document in documents:
                    try:
                        # Determine resource type based on document type
                        resource_type = "image" if document.document_type == 'profile' else "raw"
                        
                        # Delete from Cloudinary
                        self.delete_from_cloudinary(document.cloudinary_public_id, resource_type)
                        
                        # Delete from database
                        document.delete()
                        deleted_count += 1
                        
                    except Exception as e:
                        logger.error(f"Failed to delete document {document.id}: {str(e)}")
                        failed_count += 1
                
                return Response({
                    'message': f'Deleted {deleted_count} documents successfully',
                    'failed': failed_count
                }, status=status.HTTP_200_OK)

        except Document.DoesNotExist:
            return Response({
                'error': 'Document not found'
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            logger.error(f"Error during document deletion: {str(e)}")
            return Response({
                'error': f'Failed to delete document(s): {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)