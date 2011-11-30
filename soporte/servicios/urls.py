from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from servicios.views import close_services,list_user,service_reques,keep,list_service,logout_view,care_services,closed,test


urlpatterns = patterns('servicios.views',
    # Example:
    # (r'^soporte/', include('soporte.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^cerrar_servicios/(?P<data>.*)$', close_services),
    (r'^cerrar/$', closed),
    (r'^listar/$', test),
    (r'^service_request/$',service_reques),
    (r'^saved/$',keep),
    (r'^list_services/$',list_service),
    #(r'^direcion que se pone en la barra de url en el navegador/$',nombre de la vista que contiene el controlador),
    (r'^login/$',"login_view"),
    (r'^logout/$',"logout_view"),
    (r'^accounts/login/$', 'login_view'),
    (r'^care_service/(?P<service>.*)$', care_services),
    url( r'^$', 'index', name = 'demo_index' ),
    url( r'^users/$', 'ajax_user_search', name = 'demo_user_search'),
  
)
