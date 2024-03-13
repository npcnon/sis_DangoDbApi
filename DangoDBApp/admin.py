

# Register your models here.
from django.contrib import admin
from .models import TblRoomInfo,TblCourse,TblDepartment

# Register the TblRoomInfo model with the admin site
admin.site.register(TblRoomInfo)
admin.site.register(TblCourse)
admin.site.register(TblDepartment)
