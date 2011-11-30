from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

#from servicios.views import crear_servicios,list_user,service_reques,keep,list_service,logout_view,care_services


urlpatterns = patterns('',
    # Example:
    # (r'^soporte/', include('soporte.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT} ),
    (r'^',include('soporte.servicios.urls')),
)
