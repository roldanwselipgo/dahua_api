from django import forms
from .models import Device

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['ip', 'puerto', 'usuario', 'password']
        widgets = {
            'usuario': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Usuario'}),
            'password': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}),
            'ip': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ip '}),
            'puerto': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Puerto  '}),
        }
        labels = {
           'ip':'', 'puerto':'' , 'usuario':'', 'password': '',
        }

class DefaultConfigForm(forms.Form):
    Compression = forms.CharField(label = "Compression", required=True, widget=forms.TextInput(
        attrs={'class':'', 'placeholder':'Compression'}
    ))
    resolution = forms.CharField(label = "resolution", required=True, widget=forms.TextInput(
        attrs={'class':'', 'placeholder':'resolution'}
    ))
    SmartCodec = forms.CharField(label = "SmartCodec", required=True, widget=forms.TextInput(
        attrs={'class':'', 'placeholder':'SmartCodec'}
    ))
    FPS = forms.CharField(label = "FPS", required=True, widget=forms.TextInput(
        attrs={'class':'', 'placeholder':'FPS'}
    ))
    BitRateControl = forms.CharField(label = "BitRateControl", required=True, widget=forms.TextInput(
        attrs={'class':'', 'placeholder':'BitRateControl'}
    ))
    Quality = forms.CharField(label = "Quality", required=True, widget=forms.TextInput(
        attrs={'class':'', 'placeholder':'Quality'}
    ))
    BitRate = forms.CharField(label = "BitRate", required=True, widget=forms.TextInput(
        attrs={'class':'', 'placeholder':'BitRate'}
    ))
    Language = forms.CharField(label = "Language", required=True, widget=forms.TextInput(
        attrs={'class':'', 'placeholder':'Language'}
    ))
    VideoEnable = forms.CharField(label = "VideoEnable", required=True, widget=forms.TextInput(
        attrs={'class':'', 'placeholder':'VideoEnable'}
    ))  
    CurrentTime = forms.CharField(label = "CurrentTime", required=True, widget=forms.TextInput(
        attrs={'class':' input-current', 'placeholder':'Y-m-d H:M:S', 'disabled':'true'}
    ))  