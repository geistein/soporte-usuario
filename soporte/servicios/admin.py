import models
from django.contrib import  admin
from soporte.servicios.models import Services,Provider

class ServiciosAdmin(admin.ModelAdmin):
    list_display=('clients','application_date','dependence',)
    search_fields = ('description_failure',)


admin.site.register(Services,ServiciosAdmin) 
admin.site.register(Provider)
