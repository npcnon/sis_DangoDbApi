#DangoDBForWinforms.urls

from django.contrib import admin
from django.urls import path, include
from .views import display_all_data

urlpatterns = [
    path('alldata/', display_all_data, name='all_data'),
    path('admin/', admin.site.urls),
    path('api/', include('DangoDBApp.urls')),
    path('api/', include('users.urls')),
    path('api/', include('FileApp.urls')),
]

