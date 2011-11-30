from django.db import models
from django.contrib.auth.models import User





class Clients(models.Model):
    name = models.CharField(max_length=30)  
  
    class Admin:
        pass   

    #def __unicode__(self):
        #return self.name
    def __str__(self):
        return self.name

    

    

class Provider(models.Model):
    name = models.CharField(max_length=30)

    class Admin:
        pass   

    #def __unicode__(self):
        #return self.name  
    def __str__(self):
        return self.name

    
    

class Dependence(models.Model):
    name = models.CharField(max_length=30)
    
    class Admin:
        pass   

    def __str__(self):
        return self.name  


class TechnicalConcept(models.Model):
    description = models.CharField(max_length=30)
    

    
    class Admin:
        pass    

    def __str__(self):
        return self.description  






class Services(models.Model):
    clients = models.ForeignKey(Clients,default= 0)
    provider = models.ForeignKey(User,default= 0)
    technical_concept=models.ForeignKey(TechnicalConcept,default= 0)
    dependence = models.ForeignKey(Dependence,default= 0)
    application_date = models.DateTimeField(auto_now_add
=True)
    service_start_date = models.DateTimeField(blank = True,null=True)
    service_end_date = models.DateTimeField(blank = True,null=True)
    description_failure = models.TextField(max_length=300)
    work_made = models.TextField(max_length=300)
    closed = models.BooleanField(default= False)
    state = models.BooleanField(default= False)
  

    class Admin:
        pass
        list_display = ('clients','dependence','application_date','description_failure',)
        list_filter = ('application_date',)
        ordering = ('application_date',)
        search_fields = ('description_failure',)

    def __str__(self):
        
        return '%s %s %s %s' % (self.work_made, self.technical_concept, self.clients, self.service_start_date)

    def time(self):
        duration=self.service_end_date - self.service_start_date
        return duration

    def waite(self):
        waiting=self.service_start_date - self.application_date
        return waiting

    def total(self):
        absolute= self.time() + self.waite()
        return absolute

    #def __str__(self):
       # return self.servicios_conceptecnicos 


#class ServiciosConceptosTecnicos(models.Model):
    #servicios_id = models.ForeignKey(Servicios)
    #conceptotecnico_id = models.ForeignKey(ConceptoTecnico)




