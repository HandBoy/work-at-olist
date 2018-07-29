from django.contrib import admin
from .models import Call, CallEnd, CallStart

# Register your models here.
admin.site.register(Call)
admin.site.register(CallEnd)
admin.site.register(CallStart)