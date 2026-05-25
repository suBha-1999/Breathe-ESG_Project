from django.contrib import admin
from .models import Tenant, DataSource, EmissionRecord

admin.site.register(Tenant)
admin.site.register(DataSource)
admin.site.register(EmissionRecord)