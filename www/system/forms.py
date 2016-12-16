from django import forms
from system.models import ConnectedDevice


class ConnectedDeviceForm(forms.Form):
    type_chioces = (
        ('ARTIK', 'artik'),
        ('RASPBERRY PI', 'raspberry pi'),
        ('LINUX-PC', 'linux-pc'),
        ('WINDOWS-PC', 'windows-pc')
    )
    deviceType = forms.ChoiceField(widget=forms.Select,choices=type_chioces)
    ip = forms.CharField(max_length=20, required=True)
    hostname = forms.CharField(max_length=50)

    def clean(self):
        cleaned_data = super(ConnectedDeviceForm, self).clean()
        deviceType = cleaned_data.get('deviceType', '')
        ip = cleaned_data.get('ip', '')
        hostname = cleaned_data.get('hostname', '')
        if ConnectedDevice.objects.filter(ip=ip).exists():
            raise forms.ValidationError("Already exist value")
        if not ip:
            raise forms.ValidationError("Required field")
        if not deviceType:
            raise forms.ValidationError("Required field")
        return self.cleaned_data