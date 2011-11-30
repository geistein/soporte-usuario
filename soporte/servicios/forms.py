from django import forms
#from django.forms.widgets import Textarea



#aqui importo la tabla servicios de la base de datos soporte
from soporte.servicios.models import Services





        
TOPIC_CHOICES = (
                 ('general', 'General enquiry'),
                 ('bug','Bug report'),
                 ('suggestion','Suggestion'),
                 )

class ContactForm(forms.Form):
    topic = forms.ChoiceField(choices=TOPIC_CHOICES)
    message = forms.CharField(widget=forms.Textarea(),
initial="Replace with your feedback"
)
    sender = forms.EmailField(required = False, initial="user@example.com")
    
    def clean_message(self):
        message = self.cleaned_data.get('message','')
        num_words = len(message.split())
        if num_words<4:
            raise forms.ValidationError("No son suficientes palabras")
        return message  


class Service_Request(forms.ModelForm,):
    class Meta:        
        model = Services  
         
        fields = ['clients','dependence','description_failure']
    #descripcion_falla=forms.CharField(widget=forms.Textarea(attrs={'rows':'4'}))          
        	     
