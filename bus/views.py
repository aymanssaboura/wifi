import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.views.generic import ListView


from .models import Bus,Driver
from .forms import DriverForm,BusForm
from account.forms import AccountForm
from account.models import Account
from django.contrib.auth.decorators import user_passes_test
# is_MANAGER
# is_RESERVATION
# is_ACCOUNTANT
# is_CUSTOMER
@login_required
def bus_index(request):
    company = request.user.company
    buss = Bus.objects.filter(company=company).order_by('-id')
    if hasattr( request.user  ,'is_MANAGER' ) :
        accountForm = AccountForm()
        form = BusForm()
        return render(request, 'bus/bus_index.html',{'form': form,'accountForm':accountForm,'buss':buss ,'navbar':"mycompany",'submenu':"Bus's"})
    return HttpResponse(
        status=403,
        headers={
            'HX-Trigger': json.dumps({

               "customerListChanged": None,
            })
        })

@login_required
def Bus_list(request):
    company = request.user.company
    buss = bus.objects.filter(company=company).order_by('-id')
    return render(request, 'bus/bus_list.html', {
        'buss':buss
    })

@login_required
def add_buss(request):
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
        form = BusForm(request.POST,request.FILES)
        # print("request.POST: ",request.POST)
        if form.is_valid() and accountForm.is_valid():
            # print(form)
            account = accountForm.save(commit=False)
            account.company=request.user.company
            account.author=request.user
            account.account_type= '34'
            account.save()

            bus = form.save(commit=False)
            bus.author=request.user
            bus.company=request.user.company
            bus.account=account

            bus.save()

            # print(category)
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "customerListChanged": None,
                        "showMessage": f"{bus.account.name} added."
                    })
                })
        else:
            return render(request, 'bus/bus_form.html', {
        'form': form,'accountForm':accountForm
    })
    else:
        accountForm = AccountForm()
        form = BusForm()
    return render(request, 'bus/bus_form.html', {
        'form': form,'accountForm':accountForm
    })

@login_required
def edit_bus(request, pk):
    bus = get_object_or_404(Customer, pk=pk)
    account = get_object_or_404(Account , pk = customer.account.pk)
    # print('account  : ',account)
    if request.method == "POST":
        form = BusForm(request.POST,request.FILES, instance=bus)
        accountForm = AccountForm(request.POST, instance=account)
        # print(request.FILES, 'form.is_valid')

        if form.is_valid()and accountForm.is_valid():
            account = accountForm.save(commit=False)
            account.company=request.user.company
            account.author=request.user
            account.account_type='34'
            account.save()
            # print("form",form )
            bus = form.save(commit=False)
            bus.author=request.user
            bus.company=request.user.company
            bus.account=account

            bus.save()


            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "customerListChanged": None,
                        "showMessage": f"{bus.account.name} updated."
                    })
                }
            )
    else:
        form = BusForm(instance=customer)
        accountForm = AccountForm(instance=account)
        # print('form   :  ',form)
    return render(request, 'bus/bus_form.html', {
        'form': form,'accountForm':accountForm,
        'bus': bus,
    })

@login_required
@ require_POST
def remove_bus(request, pk):
    bus = get_object_or_404(bus, pk=pk)
    account = get_object_or_404(Account , pk = bus.account.pk)
    account.soft_delete()
    bus.soft_delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "customerListChanged": None,
                "showMessage": f"{bus.account.name} deleted."
            })
        })







@login_required
def driver_index(request):
    company = request.user.company
    drivers = Bus.objects.filter(company=company).order_by('-id')
    if hasattr( request.user  ,'is_MANAGER' ) :
        accountForm = AccountForm()
        form = DriverForm()
        return render(request, 'driver/driver_index.html',{'form': form,'accountForm':accountForm,'driver':drivers ,'navbar':"mycompany",'submenu':"driver's"})
    return HttpResponse(
        status=403,
        headers={
            'HX-Trigger': json.dumps({

               "customerListChanged": None,
            })
        })

@login_required
def driver_list(request):
    company = request.user.company
    drivers = Driver.objects.filter(company=company).order_by('-id')
    return render(request, 'driver/driver_list.html', {
        'drivers':drivers
    })

@login_required
def add_driver(request):
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
        form = DriverForm(request.POST,request.FILES)
        # print("request.POST: ",request.POST)
        if form.is_valid() and accountForm.is_valid():
            # print(form)
            account = accountForm.save(commit=False)
            account.company=request.user.company
            account.author=request.user
            account.account_type= '35'
            account.save()

            driver = form.save(commit=False)
            driver.author=request.user
            driver.company=request.user.company
            driver.account=account

            driver.save()

            # print(category)
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "customerListChanged": None,
                        "showMessage": f"{driver.account.name} added."
                    })
                })
        else:
            return render(request, 'driver/driver_form.html', {
        'form': form,'accountForm':accountForm
    })
    else:
        accountForm = AccountForm()
        form = DriverForm()
    return render(request, 'driver/driver_form.html', {
        'form': form,'accountForm':accountForm
    })

@login_required
def edit_driver(request, pk):
    Driver = get_object_or_404(Driver, pk=pk)
    account = get_object_or_404(Account , pk = driver.account.pk)
    # print('account  : ',account)
    if request.method == "POST":
        form = BusForm(request.POST,request.FILES, instance=driver)
        accountForm = AccountForm(request.POST, instance=account)
        # print(request.FILES, 'form.is_valid')

        if form.is_valid()and accountForm.is_valid():
            account = accountForm.save(commit=False)
            account.company=request.user.company
            account.author=request.user
            account.account_type='35'
            account.save()
            # print("form",form )
            driver = form.save(commit=False)
            driver.author=request.user
            driver.company=request.user.company
            driver.account=account

            driver.save()


            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "customerListChanged": None,
                        "showMessage": f"{driver.account.name} updated."
                    })
                }
            )
    else:
        form = DriverForm(instance=driver)
        accountForm = AccountForm(instance=account)
        # print('form   :  ',form)
    return render(request, 'driver/driver_form.html', {
        'form': form,'accountForm':accountForm,
        'driver': driver,
    })

@login_required
@ require_POST
def remove_driver(request, pk):
    bus = get_object_or_404(bus, pk=pk)
    account = get_object_or_404(Account , pk = driver.account.pk)
    account.soft_delete()
    driver.soft_delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "customerListChanged": None,
                "showMessage": f"{driver.account.name} deleted."
            })
        })

