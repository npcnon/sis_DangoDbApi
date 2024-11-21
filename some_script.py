import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DangoDBForWinforms.settings")
django.setup()

from DangoDBApp.models import TblProspectus
from DangoDBApp.models import TblStudentBasicInfo as t
from DangoDBApp.models import TblStudentPersonalData as p
from users.models import User as u
email = "npc0"
all_tables = [p]
for x in all_tables:
    x.objects.filter(email__icontains=email).delete()



# from transformers import pipeline

# # Load a conversational pipeline
# chatbot = pipeline('conversational', model='microsoft/DialoGPT-medium')

# # Generate a response
# response = chatbot("Hello! How can I help you?")
# print(response)
