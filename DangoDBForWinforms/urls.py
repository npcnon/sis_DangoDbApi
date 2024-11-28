from django.contrib import admin
from django.urls import path, include
from .views import display_all_data
from django.http import HttpResponse

def health_check(request):
    return HttpResponse("Hello World")

urlpatterns = [
    path('', health_check, name='health_check'),  # Base URL for uptime robot
    path('alldata/', display_all_data, name='all_data'),
    path('admin/', admin.site.urls),
    path('api/', include('DangoDBApp.urls')),
    path('api/', include('users.urls')),
    path('api/', include('FileApp.urls')),
]