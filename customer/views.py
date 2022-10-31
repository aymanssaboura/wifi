import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.db.models import Q # new
from .models import Customer
from .forms import CustomerForm
from account.forms import AccountForm
from account.models import Account
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
    customers = Customer.objects.filter(company=company).order_by('-id')
    if hasattr( request.user  ,'is_MANAGER' ) :
        accountForm = AccountForm()
        form = CustomerForm()
        return render(request, 'customer/index.html',{'form': form,'accountForm':accountForm,'customers':customers ,'navbar':"Company",'submenu':""})
    return HttpResponse(
        status=403,
        headers={
            'HX-Trigger': json.dumps({

               "customerListChanged": None,
            })
        })

@login_required
def customer_list(request):
    company = request.user.company
    customers = Customer.objects.filter(company=company).order_by('-id')
   
   
    vall=request.GET.get('All','true')
    vclient=request.GET.get('client','true')
    vbackage=request.GET.get('backagecompany','true')
    vair=request.GET.get('aircompany','true')
    vtrans=request.GET.get('transportcompany','true')
    vferry=request.GET.get('seacompany','true')
    vvisa=request.GET.get('visacompany','true')
    vhotel=request.GET.get('hotelcompany','true')
    vinsurance=request.GET.get('insurancecompany','true')
    vdocument=request.GET.get('documentcompany','true')
    vshipping=request.GET.get('shippingcompany','true')


    if len(vall) == 0 :
       customers = Customer.objects.filter(company=company).order_by('-id')
    if len(vclient) == 0:
       customers= customers.filter(client=True)      
    if len(vbackage) == 0:
       customers= customers.filter(backagecompany=True)  
    if len(vair) == 0:
       customers= customers.filter(aircompany=True)      
    if len(vtrans) == 0:
       customers= customers.filter(transportcompany=True)      
    if len(vferry) == 0:
       customers= customers.filter(seacompany=True)  
    if len(vvisa) == 0:
       customers= customers.filter(visacompany=True) 
    if len(vhotel) == 0:
       customers= customers.filter(hotelcompany=True)      
    if len(vinsurance) == 0:
       customers= customers.filter(insurancecompany=True)  
    if len(vdocument) == 0:
       customers= customers.filter(documentcompany=True)    
    if len(vshipping) == 0:
       customers= customers.filter(shippingcompany=True) 
    return render(request, 'customer/customer_list.html', {
        'customers':customers
    })

@login_required
def add_customer(request):
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
                        "showMessage": f"{customer.account.name} added.",
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

@login_required
def edit_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    account = get_object_or_404(Account , pk = customer.account.pk)
    # print('account  : ',account)
    if request.method == "POST":
        form = CustomerForm(request.POST,request.FILES, instance=customer)
        accountForm = AccountForm(request.POST, instance=account)
        # print(request.FILES, 'form.is_valid')

        if form.is_valid()and accountForm.is_valid():
            account = accountForm.save(commit=False)
            account.company=request.user.company
            account.author=request.user
            account.account_type='20'
            account.save()
            # print("form",form )
            customer = form.save(commit=False)
            customer.author=request.user
            customer.company=request.user.company
            customer.account=account

            customer.save()


            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "customerListChanged": None,
                        "showMessage": f"{customer.account.name} updated."
                    })
                }
            )
    else:
        form = CustomerForm(instance=customer)
        accountForm = AccountForm(instance=account)
        # print('form   :  ',form)
    return render(request, 'customer/customer_form.html', {
        'form': form,'accountForm':accountForm,
        'customer': customer,
    })

@login_required
@ require_POST
def remove_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    account = get_object_or_404(Account , pk = customer.account.pk)
    account.soft_delete()
    customer.soft_delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "customerListChanged": None,
                "showMessage": f"{customer.account.name} deleted."
            })
        })


