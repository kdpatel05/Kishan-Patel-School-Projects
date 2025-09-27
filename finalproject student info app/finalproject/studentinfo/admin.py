from django.contrib import admin
from studentinfo.models import Studentdetails, Coursedetails # Import Studentdetails and Coursedetails models

# Register your models here.

admin.site.register(Studentdetails)
admin.site.register(Coursedetails)