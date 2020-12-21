from django.contrib import admin
from .models import Review,Comment 
# 관리자 권한 부여 

# Register your models here.

admin.site.register(Review)
admin.site.register(Comment)