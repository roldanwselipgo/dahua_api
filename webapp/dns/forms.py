from django import forms
from .models import DNS

class DNSForm(forms.ModelForm):
    class Meta:
        model = DNS
        fields = ['hostname', 'ip']
        widgets = {
            'hostname': forms.TextInput(attrs={'class':'form-control', 'placeholder':'hostname '}),
            'ip': forms.TextInput(attrs={'class':'form-control', 'placeholder':'ip  '}),
        }
        labels = {
           'hostname':'', 'ip':'' , 
        }
