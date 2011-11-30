from django.template.loader  import  get_template
from django.template import loader,Context
from django.template import Context,RequestContext
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.shortcuts import render_to_response
from soporte.servicios.forms import ContactForm,Service_Request
#from soporte.servicios.models import Clientes
from models import Clients,Services,Dependence,Provider,TechnicalConcept
from django.db.models import Q
#from forms import ContactForm
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.utils import simplejson as json
from django_excel_templates import *
import time
import csv
import datetime
from searches import Search



import datetime
#import MySQLdb

#def list_user(request):
    #db= MySQLdb.connect(user='root',db='soporte',passwd='root',host='localhost')
    #cursor = db.cursor()
    #cursor.execute('SELECT nombre FROM servicios_clientes')
    #nombres = [row[0]for row in cursor.fetchall()]
    #db.close()
    #return render_to_response('list  _user.html',{'nombres':nombres})

def list_user(request):
    nombres = Clientes.objects.order_by('nombre')
    return render_to_response('list_user.html',{'nombres':nombres})

def test(request):
    #shipping = envio "variable"
    shipping= Search().searching()
    dates=list(shipping)
    cont = len(dates)
    return render_to_response("list_user.html", {'send':dates,'cont':cont})

"""def show_excel(request):
    election = Servicios.objects.all()

    for i in election:
        ballots = i 
    # Flatten candidate list after converting QuerySets into lists
    
    tiempo = ballots.fecha_fin_servicio-ballots.fecha_ini_servicio
    
    response = render_to_response("list_user.html", {
        'ballots': ballots.trabajo_realizado, 'descripcion':ballots.descripcion_falla, 'tiempo':tiempo
    })
    filename = "election%s.xls" % (ballots.trabajo_realizado)
    response['Content-Disposition'] = 'attachment; filename='+filename
    response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'

    return response"""
    

        
@login_required(redirect_field_name='/accounts/login/')
def close_services(request,data):
   
    #prestador = Prestador.objects.all()
    #arreglo1 =[]
    #aqui hago un arreglo(lista) y envio arreglo1
    #for a in prestador:
        #arreglo2 = []
        #arreglo2.append(a.id)
        #arreglo2.append(a.nombre)
        #arreglo1.append(arreglo2)

#aqui hago un objeto
    technicalconcept=TechnicalConcept.objects.all()

      #dos formas de enviar datos de una tabla como objeto o arreglo(lista),como arreglo seria: arreglo1, y como objeto seria: prestador
    return render_to_response('cerrar_servicio.html', {'tecnico':technicalconcept,'data':data})


def closed(request):
    
    if request.method == "POST":
        id_servicio = request.POST['todo[id]']
        #id_prestador = request.POST['todo[dato]']
        service = Services.objects.get(id=id_servicio)
        """Este bloque guarda en la tabla ServiciosConceptosTecnicos los datos
            que se envian de un select en modo de si se han seleccionado varios
         
        id_concepto=[]         
        for a in range(len(request.POST.getlist('tecno'))):
            id_concepto.append(request.POST.getlist('tecno')[a])
        for i in range(len(id_concepto)):
            tecnico=ServiciosConceptosTecnicos(conceptotecnico_id_id=id_concepto[i],servicios_id_id=id_servicio)
            tecnico.save()"""
        id_concepto = request.POST['tecno']
        trabajo_realizado = request.POST['todo[texto]']        
        #service.prestador_id = id_prestador
        service.technical_concept_id = id_concepto
        service.service_end_date = datetime.datetime.now()
        service.work_made = trabajo_realizado
        service.closed = True
        service.save()
        respuesta = Services.objects.get(id=id_servicio)

        """Este es otro bloque que utiliza la tabla ServiciosConceptosTecnicos para traer los datos del servicio        presente hacer la busqueda en ServiciosConceptosTecnicos y ver cuales conceptos tecnicos se hicieron en ese servicio.
        #al parecer aqui ponemos servicios_id y no servicios_id_id por que como esta mandando a buscar con el filter y no guardando como que pasa por la clase donde se crea el modelo de la tabla y toma el campo como esta alli en la clase del modelo.
 
        
        conceptos = ServiciosConceptosTecnicos.objects.filter(servicios_id = id_servicio)
        otros=[]
        for b in range(len(conceptos)):
            otros.append(conceptos[b].conceptotecnico_id_id)
        result=[]  
        for c in range(len(otros)):
            result.append(ConceptoTecnico.objects.filter(id = otros[c]))"""
        result = TechnicalConcept.objects.filter(id = service.technical_concept_id) 
        cliente = Clients.objects.filter(id = service.clients_id)
        dependencia = Dependence.objects.filter(id = service.dependence_id) 
        prestador = User.objects.filter(id = service.provider_id)
        return render_to_response('cerrado.html', {'us':result,  'datos':service, 'cliente':cliente, 'dependencia':dependencia, 'prestador':prestador})

@login_required(redirect_field_name='/accounts/login/')
def service_reques(request):
    if request.method == 'POST':    
        formulario_servicios = Service_Request(request.POST)
        if formulario_servicios.is_valid(): 
            formulario_servicios.save()#.save() es un atributo de los formulario en python todo se maneja como objetos por lo tanto los formularios son objetos que a mi parecer guarda de una lo que se recibio por post del formulario 
            return HttpResponseRedirect('/saved/')
    else:        
        formulario_servicios = Service_Request()
    
    return render_to_response('pedir_servicio.html', {'formulario': formulario_servicios})

@login_required(redirect_field_name='/accounts/login/')
def keep(request):

    #if request.method == 'POST':    
        #formulario_servicios = Service_Request(request.POST)
        #if formulario_servicios.is_valid():       
            #formulario_servicios.save()
    #last_service = Servicios.objects.count()
    for x in Services.objects.all():
        last_service = x  
        
    last_client=Clients.objects.get(id=last_service.clients_id)
    last_dependency=Dependence.objects.get(id=last_service.dependence_id)  
    #else:        
        #formulario_servicios = Service_Request()
    
    return render_to_response('service_saved.html',{'last_service':last_service,'cliente':last_client,'dependencia':last_dependency})

@login_required(redirect_field_name='/accounts/login/')
def list_service(request):
    
    if request.user.is_staff:
        us= request.user.is_staff
        id = request.user.id
    else:
        us= request.user.is_staff
    if Services.objects.all():
        service = Services.objects.filter(closed=False)
        cliente = Clients.objects.all()
        dependencia =Dependence.objects.all() 
        if service:
            presta_servicio = User.objects.all()
            if request.user.is_superuser :
                return render_to_response('list_service.html',{'service':service, 'cliente':cliente, 'dependencia':dependencia, 'prestador': presta_servicio,'id':id})
            else:
                if us == True:
                    service_prestador = Services.objects.filter(closed=False, provider= id, state= True)
                    return render_to_response('list_service.html',{'service':service_prestador, 'cliente':cliente, 'dependencia':dependencia, 'prestador': presta_servicio,'id':id})
                else:
                    mensage='Usted es un usuario sin acceso a esta parte'
                    return render_to_response('list_service.html',{'mensage':mensage})
        else:
            mensage='no hay mensajes pendientes'
            return render_to_response('list_service.html',{'mensage':mensage})
            
    else:
        mensage='no hay datos en la tabla'
        return render_to_response('list_service.html',{'mensage':mensage})

def login_view(request):
    form = AuthenticationForm()
    response  = {"form": form}
    response.update(csrf(request))
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render_to_response("demo.html", {'login':login,'user':user})
            else:
                response.update({"error": "usuario inactivo"})
                return render_to_response("login_demo.html", response)
        else:
            response.update({"error": "el usuario o la clave no existe"})
            return render_to_response("login_demo.html", response)

    else:
        return render_to_response("login_demo.html", response)
    return user

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')

@login_required(redirect_field_name='/accounts/login/')
def care_services(request,service):
    #if request.user.is_staff:
        #us = request.user.is_staff
    #else:
        #us = request.user.is_staff
    dato = Services.objects.get(id=service)
    #date.estado=False
    #date.save()
    if dato.state == False :
        if request.method == "POST":
            prestador = request.POST['prestador_id']
            dato.state=True
            dato.service_start_date = datetime.datetime.now()
            dato.provider_id = prestador
            dato.save()
            #en el colorbox en atender servicios la pagina que sale es  cerrar_servicio.html
            return HttpResponse(json.dumps({'access': True,'estado':dato.state,'id':dato.id}))
    else:
        return HttpResponse(json.dumps({'access': True,'id':dato.id}))


@login_required(redirect_field_name='/accounts/login/')
def index( request ):    
    template = 'index.html'
    data = {
    }
    return render_to_response( template, data, 
                               context_instance = RequestContext( request ) )

def ajax_user_search( request ):
    if request.is_ajax():
        q = request.GET.get( 'q' )
        if q is not None:            
            results = Services.objects.filter( 
                Q( id__contains = q ))
            
            template = 'results.html'
            data = {
                'results': results,
            }
            return render_to_response( template, data, 
                                       context_instance = RequestContext( request ) )





    
