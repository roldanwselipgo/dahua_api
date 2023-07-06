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

"""
class ConfigForm(forms.Form):
    Compression = forms.CharField(label = "Compression", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Compression'}
    ))
    resolution = forms.CharField(label = "resolution", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'resolution'}
    ))
    SmartCodec = forms.CharField(label = "SmartCodec", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'SmartCodec'}
    ))
    FPS = forms.CharField(label = "FPS", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'FPS'}
    ))
    BitRateControl = forms.CharField(label = "BitRateControl", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'BitRateControl'}
    ))
    Quality = forms.CharField(label = "Quality", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Quality'}
    ))
    BitRate = forms.CharField(label = "BitRate", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'BitRate'}
    ))
    Language = forms.CharField(label = "Language", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Language'}
    ))
    VideoEnable = forms.CharField(label = "VideoEnable", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'VideoEnable'}
    ))  
    CurrentTime = forms.CharField(label = "CurrentTime", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'CurrentTime'}
    ))  
"""
        
class ConfigForm(forms.Form):
    Compression = forms.CharField(label = "Compression", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Compression'}
    ))
    resolution = forms.CharField(label = "resolution", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'resolution'}
    ))
    SmartCodec = forms.CharField(label = "SmartCodec", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'SmartCodec'}
    ))
    FPS = forms.CharField(label = "FPS", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'FPS'}
    ))
    BitRateControl = forms.CharField(label = "BitRateControl", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'BitRateControl'}
    ))
    Quality = forms.CharField(label = "Quality", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Quality'}
    ))
    BitRate = forms.CharField(label = "BitRate", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'BitRate'}
    ))
    Language = forms.CharField(label = "Language", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Language'}
    ))
    VideoEnable = forms.CharField(label = "VideoEnable", required=True, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'VideoEnable'}
    ))  
    CurrentTime = forms.CharField(label = "CurrentTime", required=True, widget=forms.TextInput(
        attrs={'class':'form-control input-current', 'placeholder':'Y-m-d H:M:S'}
    ))  