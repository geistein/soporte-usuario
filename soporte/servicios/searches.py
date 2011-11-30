from models import Services,Clients


class Search(Services,Clients):

    "Para realizar busquedas de todo tipo"
    
    def __init__(self):
        Services.__init__(self)
       


    def searching(self):
        
        answer = Services.objects.all()
       
      
         
            
        #setattr(respuesta,'hora',hora)
      
           
            
        """respuesta =Clientes.objects.select_related('servicios_set')
        dato=[]
        for i in respuesta:
            if Servicios.objects.filter(clientes=i.id):
                dato.append(Servicios.objects.filter(clientes=i.id))"""
        return answer




