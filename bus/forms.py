from django import forms
from .models import Driver,Bus
from django.forms import ModelForm, DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column



class BusForm(forms.ModelForm):

    class Meta:
        model = Bus
        fields = ['start_date','busType','busNumber','seats','memo']


class DriverForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ['status','phoneNumber','phoneNumber1','start_date']        



 