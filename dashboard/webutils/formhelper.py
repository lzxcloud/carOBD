from django import forms

class SettingForm(forms.Form):
    displacemen = forms.FloatField(required=True, min_value=0.1, max_value=12)
    address = forms.CharField(required=True)