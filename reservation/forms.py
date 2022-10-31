from .models import *
from django import forms
from django.forms.models import inlineformset_factory

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = (
            'title','Date','customer'
        )
        widgets = {
            'Date': forms.DateTimeInput(format='%Y-%m-%d', attrs={'type': 'datetime-local'}),
        }



class SubreservationForm(forms.ModelForm):
    class Meta:
        model=SubReservation
        fields = (
            'reservation_type','Itemscount','private_no1','private_no2',
            'departure_date','return_date','mother_company','flight_no',
            'city1','city2','roundtrip','trip_type','supplier',
            'pay_price','pay_coin','sell_price','sell_coin','status'
        )

FormSet = inlineformset_factory(
    Reservation,
    SubReservation,
    form=SubreservationForm,
    min_num=2,  # minimum number of forms that must be filled in
    extra=1,  # number of empty forms to display
    can_delete=False  # show a checkbox in each form to delete the row
)