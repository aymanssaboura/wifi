import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from django.views.generic import ListView
from django.http.response import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from django.db.models import Q # new
from .models import Reservation,SubReservation
from .forms import ReservationForm,SubreservationForm
from customer.forms import CustomerForm
from customer.models import Customer
from django.contrib.auth.decorators import user_passes_test
from itertools import chain
# is_MANAGER
# is_RESERVATION
# is_ACCOUNTANT
# is_CUSTOMER
@login_required
def index(request):
    company = request.user.company
    
    # if request.method=="POST":
    #     dd=request.POST.get('options11')
    #     print(dd)
    reservations = Reservation.objects.all()
    print("index")
    if hasattr( request.user  ,'is_MANAGER' ) :
        
        form = ReservationForm()
        return render(request, 'reservation/index.html',{'form': form,'reservations':reservations ,'navbar':"reservatin",'submenu':""})
    return HttpResponse(
        status=403,
        headers={
            'HX-Trigger': json.dumps({

               "reservationListChanged": None,
            })
        })

@login_required
def reservation_list(request):
    # company = request.user.company
    print("list")
    reservations = Reservation.objects.all()
    
   
    return render(request, 'reservation/reservation_list.html', {
        'reservation':reservations
    })

@login_required
def add_reservation(request):
    
    print(1)
    if not request.user.is_MANAGER:
        
        return HttpResponse(
        status=403,
        headers={
            'HX-Trigger': json.dumps({

               "reservationListChanged": None,
            })
        })
    print(4)
    if request.method == "POST":
        print(3333)
        form = ReservationForm(request.POST,request.FILES)
        if form.is_valid() :
            print(3)

            reservation = form.save(commit=False)
           
            reservation.save()

            print(2)
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "reservationListChanged": None,
                        "showMessage": f"{reservation.title} added.",
                    })
                })
        else:
            return render(request, 'reservation/reservation_form.html', {
        'form': form
    })
    
    else:
        print("not equal")
        form = ReservationForm()
    return render(request, 'reservation/reservation_form.html', {
        'form': form
    })

@login_required
def edit_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
   
    # print('account  : ',account)
    if request.method == "POST":
        form = ReservationForm(request.POST,request.FILES, instance=reservation)
       
        # print(request.FILES, 'form.is_valid')

        if form.is_valid():
           
            reservation = form.save(commit=False)
           
            reservation.save()


            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "reservationListChanged": None,
                        "showMessage": f"{reservation.title} updated."
                    })
                }
            )
    else:
        form = ReservationForm(instance=reservation)
       
    return render(request, 'reservation/reservation_form.html', {
        'form': form,'reservation': reservation,
    })

@login_required
@ require_POST
def remove_reservation(request, pk):
    reservation = get_object_or_404(reservation, pk=pk)
    
    customer.soft_delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "customerListChanged": None,
                "showMessage": f"{reservation.title} deleted."
            })
        })






def create_subreservation(request, pk):
    reservation = Reservation.objects.get(id=pk)
    subreservation = Reservation.objects.filter(reservation=reservation)
    form = subreservationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            subreservation = form.save(commit=False)
            subreservation.reservation = reservation
            subreservation.save()
            return redirect("detail-subreservation", pk=subreservation.id)
        else:
            return render(request, "reservation/reservation_form.html", context={
                "form": form
            })

    context = {
        "form": form,
        "reservation": reservation,
        "subreservation": reservation
    }

    return render(request, "create_subreservation.html", context)



    def update_subreservation(request, pk):
     subreservation = SubReservation.objects.get(id=pk)
     form = SubreservationForm(request.POST or None, instance=subreservation)

     if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("detail-subreservation", pk=subreservation.id)

     context = {
        "form": form,
        "subreservation": subreservation
     }

     return render(request, "subreservation_form.html", context)


def delete_subreservation(request, pk):
    subreservation = get_object_or_404(subreservation, id=pk)

    if request.method == "POST":
        subreservation.delete()
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )


def detail_subreservation(request, pk):
    subreservation = get_object_or_404(subreservation, id=pk)
    context = {
        "subreservation": subreservation
    }
    return render(request, "subreservation_detail.html", context)


def create_subreservation_form(request):
    form = SubreservationForm()
    context = {
        "form": form
    }
    return render(request, "subreservation_form.html", context)
