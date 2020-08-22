from django.contrib import admin
from .models import Student, Application, Offer
# Register your models here.

# admin.site.register(testmodel)
admin.site.register(Student)
admin.site.register(Application)
admin.site.register(Offer)