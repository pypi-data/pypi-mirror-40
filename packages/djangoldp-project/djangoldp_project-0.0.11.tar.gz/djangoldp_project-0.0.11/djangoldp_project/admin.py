from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from .models import Project, Customer

admin.site.register(Project, GuardedModelAdmin)
admin.site.register(Customer)
