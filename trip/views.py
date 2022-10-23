from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar

from .models import *
from .utils import Calendar
from .forms import TripForm , Locationform



def index(request):
    return render(request, 'cal/calendar1.html')

class CalendarView(generic.ListView):
    model = Trip
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        city = self.request.GET.get('location', None)
        cal = Calendar(d.year, d.month,city)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['locations'] = Location.objects.all()
        context['city'] = city

        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def trip_(request, trip_id=None):
    # print("xxxxxxxxx ")
    instance = Trip()
    if trip_id:
        instance = get_object_or_404(Trip, pk=trip_id)
    else:
        instance = Trip()

    form = TripForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'cal/event.html', {'form': form})
    # return HttpResponse('hello')


@login_required
def add_location(request):
    if not request.user.is_MANAGER:
        return HttpResponse(
        status=403,
        headers={
            'HX-Trigger': json.dumps({

               "locationListChanged": None,
            })
        })
    if request.method == "POST":
        form = Locationform(request.POST)
        if request.POST:
            if form.is_valid()  :
               Location = form.save(commit=False)
               Location.save()
           
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "locationListChanged": None,
                        "showMessage": f"{Location.location} added."
                    })
                })
        else:
            return render(request, 'add_location.html', {'form': form})
    else:
        
        form = Locationform()    
    return render(request, 'add_location.html', {
        'form': form })


@login_required
def new_flight(request):
    if not request.user.is_MANAGER:
        return HttpResponse(
        status=403,
        headers={
            'HX-Trigger': json.dumps({

               "customerListChanged": None,
            })
        })
    if request.method == "POST":
        accountForm = AccountForm(request.POST)
        form = CustomerForm(request.POST,request.FILES)
        # print("request.POST: ",request.POST)
        if form.is_valid() and accountForm.is_valid():
            # print(form)
            account = accountForm.save(commit=False)
            account.company=request.user.company
            account.author=request.user
            account.account_type= '20'
            account.save()

            customer = form.save(commit=False)
            customer.author=request.user
            customer.company=request.user.company
            customer.account=account

            customer.save()

            # print(category)
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "customerListChanged": None,
                        "showMessage": f"{customer.account.name} added."
                    })
                })
        else:
            return render(request, 'customer/customer_form.html', {
        'form': form,'accountForm':accountForm
    })
    else:
        accountForm = AccountForm()
        form = CustomerForm()
    return render(request, 'customer/customer_form.html', {
        'form': form,'accountForm':accountForm
    })