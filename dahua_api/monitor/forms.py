from django import forms
from .models import Camera

class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = ['serial_no','usuario', 'password', 'ip', 'puerto','videoencode_config_id']
        widgets = {
            'serial_no': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Numero de Serie'}),
            'usuario': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Usuario'}),
            'password': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}),
            'ip': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Url  '}),
            'puerto': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Puerto  '}),
            'videoencode_config_id': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Configuracion Video'}),
        }
        labels = {
            'serial_no':'','usuario':'', 'ip':'', 'password': '','puerto':'','videoencode_config_id': '',
        }

class VideoEncodeForm():
    Compression = forms.CharField(label = "Compression", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Compression'}
    ))
    CustomResolutionName = forms.CharField(label = "CustomResolutionName", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'CustomResolutionName'}
    ))

        
