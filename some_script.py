import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DangoDBForWinforms.settings")
django.setup()

from DangoDBApp.models import TblProspectus

TblProspectus.objects.filter().delete()





# from transformers import pipeline

# # Load a conversational pipeline
# chatbot = pipeline('conversational', model='microsoft/DialoGPT-medium')

# # Generate a response
# response = chatbot("Hello! How can I help you?")
# print(response)
